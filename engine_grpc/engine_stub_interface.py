from enum import Enum, auto
from .engine_pipe_abstract import EnginePlatform

GRPC_INTERFACE_METHOD_HEADER = 'method'
GRPC_INTERFACE_PROPERTY_HEADER = 'property'


class GRPCInterface(Enum):

    # declare method interface
    method_system_get_projectinfo = auto()
    method_scene_clone = auto()

    # UnityEditor built-in static method
    method_unity_editor_import_asset = auto()
    method_unity_editor_move_asset = auto()
    method_unity_editor_assetdatabase_refresh = auto()
    method_unity_editor_assetdatabase_copy_asset = auto()
    method_unity_editor_assetdatabase_guid_to_path = auto()
    method_unity_editor_assetdatabase_find_assets = auto()
    method_unity_editor_assetdatabase_get_dependencies = auto()

    method_unity_editor_scenemanager_open = auto()
    method_unity_editor_scenemanager_save = auto()

    # prefab utilities
    method_unity_prefab_create = auto()
    method_unity_prefab_merge = auto()
    method_unity_prefab_add_component = auto()
    method_unity_prefab_set_value = auto()
    method_unity_prefab_set_reference_value = auto()
    method_unity_prefab_create_mesh_collider_object = auto()

    # material utilities
    method_unity_material_update_textures = auto()


INTERFACE_MAPPINGS = {
    GRPCInterface.method_system_get_projectinfo: {
        EnginePlatform.unity: "UGrpc.SystemUtils.GetProjectInfo"
    },
    GRPCInterface.method_scene_clone: {
        EnginePlatform.unity: "UGrpc.SceneUtils.SceneClone"
    },

    # AssetDatabase
    GRPCInterface.method_unity_editor_move_asset: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.MoveAsset"
    },
    GRPCInterface.method_unity_editor_import_asset: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.ImportAsset"
    },
    GRPCInterface.method_unity_editor_assetdatabase_refresh: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.Refresh"
    },
    GRPCInterface.method_unity_editor_assetdatabase_copy_asset: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.CopyAsset"
    },
    GRPCInterface.method_unity_editor_assetdatabase_guid_to_path: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.GUIDToAssetPath"
    },
    GRPCInterface.method_unity_editor_assetdatabase_find_assets: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.FindAssets"
    },
    GRPCInterface.method_unity_editor_assetdatabase_get_dependencies: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.GetDependencies"
    },

    # Prefab utilities
    GRPCInterface.method_unity_prefab_create: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.CreateModelAsset"
    },
    GRPCInterface.method_unity_prefab_merge: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.Merge"
    },
    GRPCInterface.method_unity_prefab_add_component: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.AddComponent"
    },
    GRPCInterface.method_unity_prefab_set_value: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.SetValue"
    },
    GRPCInterface.method_unity_prefab_set_reference_value: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.SetReferenceValue"
    },
    GRPCInterface.method_unity_prefab_create_mesh_collider_object: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.CreateMeshColliderObject"
    },

    # Scene manager
    GRPCInterface.method_unity_editor_scenemanager_open: {
        EnginePlatform.unity: "UnityEditor.SceneManagement.EditorSceneManager.OpenScene"
    },
    GRPCInterface.method_unity_editor_scenemanager_save: {
        EnginePlatform.unity: "UnityEditor.SceneManagement.EditorSceneManager.SaveScene"
    },

    # Material utilities
    GRPCInterface.method_unity_material_update_textures: {
        EnginePlatform.unity: "UGrpc.MaterialUtils.UpdateTextures"
    }
}
