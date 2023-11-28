from pickle import NONE
import pytest
from equia.models import CalculationComposition, ProblemDetails 
from equia.equia_client import EquiaClient
from equia.demofluids.demofluid1_nHexane_Ethylene_HDPE7 import demofluid1_nHexane_Ethylene_HDPE7
from utility.shared_settings import sharedsettings

@pytest.mark.asyncio
async def test_call_fluid():
    clientAdd = EquiaClient(sharedsettings.url, sharedsettings.access_key)

    inputAdd = clientAdd.get_fluid_add_input()
    inputAdd.fluid = demofluid1_nHexane_Ethylene_HDPE7()

    resultAdd: ProblemDetails = await clientAdd.call_fluid_add_async(inputAdd)

    await clientAdd.cleanup()

    #assert result.status == 400
    assert resultAdd.success == True
    
    clientGet = EquiaClient(sharedsettings.url, sharedsettings.access_key)

    inputGet = clientGet.get_fluid_get_input()
    inputGet.fluidid = resultAdd.fluidid

    resultGet: ProblemDetails = await clientGet.call_fluid_get_async(inputGet)

    await clientGet.cleanup()

    #assert result.status == 400
    assert resultGet.success == True


