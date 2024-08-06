import Items.BaseItem as BaseItem


class Material(BaseItem.Item):

    def __init__(self, item_id, name, description, base_value, rarity, weight, item_type, recipe, craft_amount, carry_limit, sprite, material_name):
        super().__init__(item_id, name, description, base_value, rarity, weight, item_type, recipe, craft_amount, carry_limit, sprite)

        self.materialName = material_name

        BaseItem.Item.materials.append(self)
        BaseItem.Item.items.append(self)





# for the next time i open this project, check the OneNote. It has the next steps for the project.


