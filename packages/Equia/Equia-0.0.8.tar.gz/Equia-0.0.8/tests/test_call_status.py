from pickle import NONE
import pytest
from equia.models import CalculationComposition, ProblemDetails 
from equia.equia_client import EquiaClient
from utility.shared_settings import sharedsettings

@pytest.mark.asyncio
async def test_call_status():
    client = EquiaClient(sharedsettings.url, sharedsettings.access_key)

    input = client.get_status_input()

    result: ProblemDetails = await client.call_status_get_async(input)

    await client.cleanup()

    #assert result.status == 400
    assert result.success == True
