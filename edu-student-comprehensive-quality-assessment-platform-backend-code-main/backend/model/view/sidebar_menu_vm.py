from infra_backbone.model.view.menu_vm import MenuViewModel


class SidebarViewModel(MenuViewModel):
    """
    侧边栏菜单
    """

    opened: bool = True
