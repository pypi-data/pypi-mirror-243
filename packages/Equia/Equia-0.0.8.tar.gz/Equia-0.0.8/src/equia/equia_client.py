import aiohttp
from typing import Any, Dict

from equia.models import StatusInput, StatusResult, CloudPointCalculationInput, CloudPointCalculationResult, \
    FlashCalculationInput, FlashCalculationResult, \
    PhasediagramFixedTemperaturePressureCalculationInput, PhasediagramFixedTemperaturePressureCalculationResult, \
    FluidAddInput, FluidAddResult, FluidGetInput, FluidGetResult, FluidDeleteInput, FluidDeleteResult, \
    SlePointCalculationInput, SlePointCalculationResult, \
    EosPropertiesTPnCalculationInput, EosPropertiesTPnCalculationResult, \
    ProblemDetails \

class EquiaClient:
    """Class for making the calling to Equia API easy"""

    def __init__(self, base_url, access_key):
        self.__base_url = "{}/publicapi/01/".format(base_url)
        self.__access_key = access_key
        self.__session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False))

    async def cleanup(self):
        """Close session"""
        await self.__session.close()

    def __append_body(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Method that appends access_key to the body of the request"""
        user = {
            "accesskey": self.__access_key,
        }
        return {**body, **user}

    async def __post_async(self, endpoint: str, json_body: Dict[str, Any], from_dict):
        """Prepare the URL and the body and makes the POST request to the API"""
        url = "{}{endpoint}".format(self.__base_url, endpoint=endpoint)
        json_body = self.__append_body(json_body)
        try:
            async with self.__session.post(url, json=json_body) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return from_dict(response)
                else:
                    return ProblemDetails.from_dict(response)
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))
            return ProblemDetails.from_dict(e)

    async def call_status_get_async(
        self,
        body: StatusInput,
    ): 
      """Return fluid with givne id"""  
      return await self.__post_async("Status/GetStatus", body.to_dict(), StatusResult.from_dict)

    async def call_fluid_get_async(
        self,
        body: FluidGetInput,
    ): 
      """Return fluid with givne id"""  
      return await self.__post_async("Fluids/GetFluid", body.to_dict(), FluidGetResult.from_dict)

    async def call_fluid_add_async(
        self,
        body: FluidAddInput,
    ): 
      """Add given fluid to web server and return fluid id"""  
      return await self.__post_async("Fluids/AddFluid", body.to_dict(), FluidAddResult.from_dict)

    async def call_fluid_delete_async(
        self,
        body: FluidDeleteInput,
    ): 
      """Delete given fluid on the web server"""  
      return await self.__post_async("Fluids/DeleteFluid", body.to_dict(), FluidDeleteResult.from_dict)

    async def call_flash_async(
        self,
        body: FlashCalculationInput,
    ):
        """Perform flash calculation"""
        return await self.__post_async("Calculations/Flash", body.to_dict(), FlashCalculationResult.from_dict)

    async def call_cloud_point_async(
        self,
        body: CloudPointCalculationInput,
    ):
        """Perform cloud point calculation"""
        return await self.__post_async("Calculations/CloudPoint", body.to_dict(), CloudPointCalculationResult.from_dict)

    async def call_sle_point_async(
        self,
        body: SlePointCalculationInput,
    ):
        """Perform SLE point calculation"""
        return await self.__post_async("Calculations/SlePoint", body.to_dict(), SlePointCalculationResult.from_dict)

    async def call_phasediagram_standard_async(
        self,
        body: PhasediagramFixedTemperaturePressureCalculationInput,
    ):
        """Perform Phasediagram standard calculation"""
        return await self.__post_async("Calculations/PhasediagramStandard", body.to_dict(), PhasediagramFixedTemperaturePressureCalculationResult.from_dict)

    async def call_eospropertiestpn_async(
        self,
        body: EosPropertiesTPnCalculationInput,
    ):
        """Perform Eos property TPn calculation"""
        return await self.__post_async("Properties/EosTPn", body.to_dict(), EosPropertiesTPnCalculationResult.from_dict)

    def get_status_input(self):
        """Returns status argument filled with standard input"""
        return StatusInput(access_key=self.__access_key)

    def get_flash_input(self):
        """Returns flash argument filled with standard input"""
        return FlashCalculationInput(access_key=self.__access_key, units=self.__get_units(), components=[], fluidid="", flashtype="Fixed Temperature/Pressure")

    def get_cloud_point_input(self):
        """Returns cloud point argument filled with standard input"""
        return CloudPointCalculationInput(access_key=self.__access_key, units=self.__get_units(), components=[], fluidid="", pointtype="Fixed Temperature")

    def get_eospropertiestpn_input(self):
        """Returns Eos property TPN argument filled with standard input"""
        return EosPropertiesTPnCalculationInput(access_key=self.__access_key, units=self.__get_units(), components=[], fluidid="", volumetype="Auto")

    def get_sle_point_input(self):
        """Returns SLE point argument filled with standard input"""
        return SlePointCalculationInput(access_key=self.__access_key, units=self.__get_units(), components=[], fluidid="", pointtype="Fixed Pressure")

    def get_phasediagam_standard_input(self):
        """Returns phase diagram standard argument filled with standard input"""
        return PhasediagramFixedTemperaturePressureCalculationInput(access_key=self.__access_key, units=self.__get_units(), components=[], fluidid="")

    def get_fluid_get_input(self):
        """Returns request fluid argument filled with standard input"""
        return FluidGetInput(access_key=self.__access_key)

    def get_fluid_add_input(self):
        """Returns new fluid argument filled with standard input"""
        return FluidAddInput(access_key=self.__access_key)

    def get_fluid_delete_input(self):
        """Returns new fluid argument filled with standard input"""
        return FluidDeleteInput(access_key=self.__access_key)

    def __get_units(self):
        return "C(In,Massfraction);C(Out,Massfraction);T(In,Kelvin);T(Out,Kelvin);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"
