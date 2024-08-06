import Items.BaseItem as BaseItem


class Armour(BaseItem.Item):

    def __init__(self, item_id, name, description, base_value, rarity, weight, item_type, armour_type, recipe, craft_amount, carry_limit, sprite, health_bonus=0, mana_bonus=0, stamina_bonus=0, staminaRecoveryBonus=0, mana_recovery_bonus=0, dodge_chance_bonus=0, armour_resistances_bonus=None):
        super().__init__(item_id, name, description, base_value, rarity, weight, item_type, recipe, craft_amount, carry_limit, sprite)

        self.healthBonus = health_bonus
        self.manaBonus = mana_bonus
        self.staminaBonus = stamina_bonus
        self.staminaRecoveryBonus = staminaRecoveryBonus
        self.manaRecoveryBonus = mana_recovery_bonus
        self.dodgeChanceBonus = dodge_chance_bonus
        self.armourType = armour_type

        # this one is a dict
        self.armourResistancesBonus = armour_resistances_bonus

        BaseItem.Item.armours.append(self)
        BaseItem.Item.items.append(self)
