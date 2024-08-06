import Items.BaseItem as BaseItem


class Weapon(BaseItem.Item):

    def __init__(self, item_id, name, description, base_value, rarity, weight, item_type, weapon_type, recipe, craft_amount, carry_limit, sprite, damage, attack_speed, crit_chance, crit_damage, armour_penetration, damage_type, effects, stamina_cost):
        super().__init__(item_id, name, description, base_value, rarity, weight, item_type, recipe, craft_amount, carry_limit, sprite)

        self.damage = damage
        self.attackSpeed = attack_speed
        self.critChance = crit_chance
        self.critDamage = crit_damage
        self.armourPenetration = armour_penetration
        self.damageType = damage_type
        self.weaponType = weapon_type
        self.effects = effects
        self.staminaCost = stamina_cost

        BaseItem.Item.weapons.append(self)
        BaseItem.Item.items.append(self)
