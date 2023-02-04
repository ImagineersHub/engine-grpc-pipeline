from ..engine_pipe_impl import SimulationEngineImpl
from ..engine_pipe_abstract import EnginePlatform
from typing import List
from ..engine_stub_interface import GRPCInterface


class UnityEngineImpl(SimulationEngineImpl):

    asset_root_folder_name: str = "Assets"

    @property
    def engine_platform(self) -> EnginePlatform:

        return EnginePlatform.unity

    def find_asset_guids(self, filter: str, paths: List[str]) -> List[str]:

        resp = self.command_parser(cmd=GRPCInterface.method_unity_editor_assetdatabase_find_assets,
                                   params=[filter,
                                           paths])
        return resp.payload

    def find_assets(self, filter: str, paths: List[str]) -> List[str]:

        guids = self.find_asset_guids(filter=filter, paths=paths)

        asset_paths = []

        for guid in guids:
            asset_paths.append(self.command_parser(cmd=GRPCInterface.method_unity_editor_assetdatabase_guid_to_path, params=[guid]).payload)

        return asset_paths
