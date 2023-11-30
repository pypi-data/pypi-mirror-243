import numpy as np
import pytest
from astropy.io import fits
from astropy.time import Time
from dkist_fits_specifications import __version__ as spec_version
from dkist_header_validator import spec214_validator
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_visp.tasks.write_l1 import VispWriteL1Frame
from dkist_processing_visp.tests.conftest import VispConstantsDb


@pytest.fixture(
    scope="function",
    params=[("HPLT-TAN", "AWAV"), ("AWAV", "HPLT-TAN")],
    ids=["correct wcs axis order", "incorrect wcs axis order"],
)
def wcs_axis_names(request):
    return request.param


@pytest.fixture
def write_l1_task(
    recipe_run_id,
    init_visp_constants_db,
    pol_type,
):
    polarimeter_mode = "observe_polarimetric"
    if pol_type == "Stokes-I":
        polarimeter_mode = "observe_intensity"
    constants_db = VispConstantsDb(
        INSTRUMENT="VISP",
        AVERAGE_CADENCE=10,
        MINIMUM_CADENCE=10,
        MAXIMUM_CADENCE=10,
        VARIANCE_CADENCE=0,
        NUM_MAP_SCANS=1,
        NUM_RASTER_STEPS=2,
        SPECTRAL_LINE="VISP Ca II H",
        POLARIMETER_MODE=polarimeter_mode,
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with VispWriteL1Frame(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:

        yield task

        task._purge()


@pytest.mark.parametrize("pol_type", ["Full Stokes", "Stokes-I"])
def test_write_l1_frame(write_l1_task, calibrated_visp_header, wcs_axis_names, pol_type, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = write_l1_task

    stokes_params = ["I", "Q", "U", "V"]
    if pol_type == "Stokes-I":
        stokes_params = ["I"]
    num_stokes = len(stokes_params)

    # Random data needed so skew and kurtosis don't barf
    hdu = fits.PrimaryHDU(
        data=np.random.random((128, 128, 1)) * 100.0, header=calibrated_visp_header
    )
    hdul = fits.HDUList([hdu])
    hdul[0].header["CTYPE1"] = wcs_axis_names[0]
    hdul[0].header["CTYPE2"] = wcs_axis_names[1]
    for i in range(num_stokes):
        task.write(
            data=hdul,
            tags=[Tag.calibrated(), Tag.frame(), Tag.stokes(stokes_params[i])],
            encoder=fits_hdulist_encoder,
        )

    task()
    for stokes_param in stokes_params:
        files = list(task.read(tags=[Tag.frame(), Tag.output(), Tag.stokes(stokes_param)]))
        assert len(files) == 1
        for file in files:
            assert file.exists
            assert spec214_validator.validate(file, extra=False)
            hdu_list = fits.open(file)
            header = hdu_list[1].header
            assert len(hdu_list) == 2  # Primary, CompImage
            assert type(hdu_list[0]) is fits.PrimaryHDU
            assert type(hdu_list[1]) is fits.CompImageHDU
            assert header["DTYPE1"] == "SPATIAL"
            assert header["DTYPE2"] == "SPECTRAL"
            assert header["DTYPE3"] == "SPATIAL"
            assert header["DAAXES"] == 2
            if len(stokes_params) == 1:
                assert "DNAXIS4" not in header
                assert header["DNAXIS"] == 3
                assert header["DEAXES"] == 1
            else:
                assert header["DNAXIS4"] == 4
                assert header["DNAXIS"] == 4
                assert header["DEAXES"] == 2
            assert header["INFO_URL"] == task.docs_base_url
            assert header["HEADVERS"] == spec_version
            assert (
                header["HEAD_URL"]
                == f"{task.docs_base_url}/projects/data-products/en/v{spec_version}"
            )
            calvers = task._get_version_from_module_name()
            assert header["CALVERS"] == calvers
            assert (
                header["CAL_URL"]
                == f"{task.docs_base_url}/projects/{task.constants.instrument.lower()}/en/v{calvers}/{task.workflow_name}.html"
            )
            calibrated_file = next(
                task.read(tags=[Tag.frame(), Tag.calibrated(), Tag.stokes(stokes_param)])
            )
            cal_header = fits.open(calibrated_file)[0].header

            # Make sure we didn't overwrite pre-computed DATE-BEG and DATE-END keys
            assert header["DATE-BEG"] == cal_header["DATE-BEG"]
            assert header["DATE-END"] == cal_header["DATE-END"]
            date_avg = (
                (Time(header["DATE-END"], precision=6) - Time(header["DATE-BEG"], precision=6)) / 2
                + Time(header["DATE-BEG"], precision=6)
            ).isot
            assert header["DATE-AVG"] == date_avg
            assert isinstance(header["HLSVERS"], str)
            assert header["PROPID01"] == "PROPID1"
            assert header["PROPID02"] == "PROPID2"
            assert header["EXPRID01"] == "EXPERID1"
            assert header["EXPRID02"] == "EXPERID2"
            assert header["EXPRID03"] == "EXPERID3"
            assert header["WAVEBAND"] == "H alpha (656.28 nm)"
            assert header["SPECLN01"] == "H alpha (656.28 nm)"
            assert header["SPECLN02"] == "Ni I (676.78 nm)"
            with pytest.raises(KeyError):
                header["SPECLN03"]
