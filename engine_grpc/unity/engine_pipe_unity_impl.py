from ..engine_pipe_impl import SimulationEngineImpl
from ..engine_pipe_abstract import EnginePlatform
from typing import List
from ..engine_stub_interface import GRPCInterface
from ugrpc_pipe import ProjectInfoResp
import os


class UnityEngineImpl(SimulationEngineImpl):

    asset_root_folder_name: str = "Assets"

    @property
    def engine_platform(self) -> EnginePlatform:

        return EnginePlatform.unity

    def find_asset_guid_list(self, filter: str, paths: List[str]) -> List[str]:

        resp = self.command_parser(cmd=GRPCInterface.method_editor_assetdatabase_find_assets,
                                   params=[filter,
                                           paths])
        return resp.payload

    def find_assets(self, filter: str, paths: List[str]) -> List[str]:

        guid_list = self.find_asset_guid_list(filter=filter, paths=paths)

        asset_paths = []

        for guid in guid_list:
            asset_paths.append(self.command_parser(cmd=GRPCInterface.method_editor_assetdatabase_guid_to_path, params=[guid]).payload)

        return asset_paths

    def get_dependencies(self, path: str, recursive: bool) -> List[str]:

        return self.command_parser(cmd=GRPCInterface.method_editor_assetdatabase_get_dependencies, params=[path, recursive]).payload

    def get_project_info(self) -> ProjectInfoResp:
        return self.command_parser(cmd=GRPCInterface.method_system_get_projectinfo).payload

    def fetch_full_path(self, path: str) -> str:
        if not path.startswith(self.asset_root_folder_name):
            raise ValueError(f"The specified path is invalid: {path}. Path should start with '{self.asset_root_folder_name}'")

        return os.path.join(self.get_project_info().project_root, path)
