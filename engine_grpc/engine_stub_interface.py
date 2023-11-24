from enum import Enum, auto
from .engine_pipe_abstract import EnginePlatform

GRPC_INTERFACE_METHOD_HEADER = 'method'
GRPC_INTERFACE_PROPERTY_HEADER = 'property'


class GRPCInterface(Enum):

    # declare method interface
    method_system_get_service_status = auto()
    method_system_get_projectinfo = auto()
    method_scene_create = auto()

    # UnityEditor built-in static method
    method_editor_import_asset = auto()
    method_editor_move_asset = auto()
    method_editor_assetdatabase_refresh = auto()
    method_editor_assetdatabase_copy_asset = auto()
    method_editor_assetdatabase_guid_to_path = auto()
    method_editor_assetdatabase_find_assets = auto()
    method_editor_assetdatabase_get_dependencies = auto()

    method_editor_scenemanager_open = auto()
    method_editor_scenemanager_save = auto()

    # prefab utilities
    method_object_create = auto()
    method_object_merge = auto()
    method_object_add_component = auto()
    """Represent the interface of adding component to the specific gameobject
    
    Example:
        PrefabUtils.AddComponent(
            source: "Assets/Content/Test.prefab",
            componentPath: "default/UnityEngine.MeshCollider, UnityEngine",
            isCreate: true
        );

    'default' is child object name. specify the component type full name and namespace

    """

    method_object_change_activate = auto()
    """Represent the interface of changing the activate state of gameobject or component.
    
    Example:
        PrefabUtils.ChangeActivate(
            source: "Assets/Content/Test.prefab",
            path: "default/UnityEngine.MeshRenderer, UnityEngine",
            isActive: true
        );

    'default' is child object name and the following is the component info. If there was no
    component specified, it would apply the activating on the gameobject only.

    """

    method_object_set_value = auto()
    method_object_set_reference_value = auto()
    method_object_create_mesh_collider_object = auto()
    method_object_create_variant = auto()
    method_object_set_active = auto()
    method_object_trim = auto()

    # material utilities
    method_material_update_textures = auto()

    method_unittest_get_float_array_data = auto()


INTERFACE_MAPPINGS = {
    GRPCInterface.method_system_get_service_status: {
        EnginePlatform.unity: "UGrpc.SystemUtils.GetServiceStatus"
    },
    GRPCInterface.method_system_get_projectinfo: {
        EnginePlatform.unity: "UGrpc.SystemUtils.GetProjectInfo"
    },
    GRPCInterface.method_scene_create: {
        EnginePlatform.unity: "UGrpc.SceneUtils.CreateScene"
    },

    # AssetDatabase
    GRPCInterface.method_editor_move_asset: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.MoveAsset"
    },
    GRPCInterface.method_editor_import_asset: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.ImportAsset"
    },
    GRPCInterface.method_editor_assetdatabase_refresh: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.Refresh"
    },
    GRPCInterface.method_editor_assetdatabase_copy_asset: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.CopyAsset"
    },
    GRPCInterface.method_editor_assetdatabase_guid_to_path: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.GUIDToAssetPath"
    },
    GRPCInterface.method_editor_assetdatabase_find_assets: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.FindAssets"
    },
    GRPCInterface.method_editor_assetdatabase_get_dependencies: {
        EnginePlatform.unity: "UnityEditor.AssetDatabase.GetDependencies"
    },

    # Prefab utilities
    GRPCInterface.method_object_create: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.CreateModelAsset"
    },
    GRPCInterface.method_object_merge: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.Merge"
    },
    GRPCInterface.method_object_add_component: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.AddComponent"
    },
    GRPCInterface.method_object_change_activate: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.ChangeActivate"
    },
    GRPCInterface.method_object_set_value: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.SetValue"
    },
    GRPCInterface.method_object_set_reference_value: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.SetReferenceValue"
    },
    GRPCInterface.method_object_create_mesh_collider_object: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.CreateMeshColliderObject"
    },
    GRPCInterface.method_object_create_variant: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.CreatePrefabVariant"
    },
    GRPCInterface.method_object_set_active: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.SetActive"
    },
    GRPCInterface.method_object_trim: {
        EnginePlatform.unity: "UGrpc.PrefabUtils.Trim"
    },

    # Scene manager
    GRPCInterface.method_editor_scenemanager_open: {
        EnginePlatform.unity: "UnityEditor.SceneManagement.EditorSceneManager.OpenScene"
    },
    GRPCInterface.method_editor_scenemanager_save: {
        EnginePlatform.unity: "UnityEditor.SceneManagement.EditorSceneManager.SaveScene"
    },

    # Material utilities
    GRPCInterface.method_material_update_textures: {
        EnginePlatform.unity: "UGrpc.MaterialUtils.UpdateTextures"
    },

    # Scene utilities
    GRPCInterface.method_material_update_textures: {
        EnginePlatform.unity: "UGrpc.MaterialUtils.UpdateTextures"
    },

    # UnitTest utilities
    GRPCInterface.method_unittest_get_float_array_data: {
        EnginePlatform.unity: "UGrpc.UnitTestUtils.GetFloatArrayData"
    }
}
