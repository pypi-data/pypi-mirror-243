from uniref import AndroidUniRef

scripts = dict()
ref = AndroidUniRef(package_name="com.ChillyRoom.DungeonShooter")


def on_message(msg, data):
    if msg["type"] != "send":
        return
    print(msg["payload"])


def gem_cheat():
    save_data = ref.find_class_in_image("Assembly-CSharp.dll", "PlayerSaveData")
    get_gems = save_data.find_method("get_gems")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                retval.replace(91821);
            }
        })
    });""".replace("ADDRESS", f"ptr({hex(get_gems.address)})")
    return ref.execute_js(code)


def fish_cheat():
    fish_controller = ref.find_class_in_image("Assembly-CSharp.dll", "FishChipStore.Config.FishChipPurchaseController")
    get_fish_count = fish_controller.find_method("get_fishCount")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                retval.replace(1000);
            }
        })
    });""".replace("ADDRESS", f"ptr({hex(get_fish_count.address)})")
    return ref.execute_js(code)


def skill_cd_cheat():
    attr = ref.find_class_in_image("Assembly-CSharp.dll", "RoleAttributePlayer")
    get_skill_ready = attr.find_method("get_skill_ready")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                retval.replace(1);
            }
        })
    });""".replace("ADDRESS", f"ptr({hex(get_skill_ready.address)})")
    return ref.execute_js(code)


def energy_cheat():
    attr = ref.find_class_in_image("Assembly-CSharp.dll", "RoleAttributePlayer")
    set_energy = attr.find_method("set_energy")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS, {
            onEnter: function(args) {
                args[1] = ptr(200);
            },
            onLeave: function(retval) { }
        })
    });""".replace("ADDRESS", f"ptr({hex(set_energy.address)})")
    return ref.execute_js(code)


def armor_cheat():
    attr = ref.find_class_in_image("Assembly-CSharp.dll", "RoleAttributePlayer")
    get_ArmorLoad = attr.find_method("get_HasArmor")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS, {
            onEnter: function(args) {
                args[0].add(0x8c).writeU32(12);
            },
            onLeave: function(retval) { }
        })
    });""".replace("ADDRESS", f"ptr({hex(get_ArmorLoad.address)})")
    return ref.execute_js(code)


def season_coin_cheat():
    season_data = ref.find_class_in_image("Assembly-CSharp.dll", "SeasonData")
    season_data.set_instance(season_data.find_field("_data").value)
    season_coin = season_data.find_field("coin")
    season_coin.value = 90000


def pay_cheat():
    classes = ref.find_image_by_name("Assembly-CSharp.dll").list_classes()
    on_purchase_done = classes[10635].find_method("<BuyItem>b__0")  # <>c__DisplayClass71_0

    mall_data = ref.find_class_in_image("Assembly-CSharp.dll", "RGScript.Data.Mall.MallData")
    after_purchase = mall_data.find_method("AfterPurchaseMallItem")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS1, {
            onEnter: function(args) {
                args[1] = ptr(1);
            },
            onLeave: function(retval) { }
        })

        Interceptor.attach(ADDRESS2, {
            onEnter: function(args) {
                args[2] = ptr(1);
            },
            onLeave: function(retval) { }
        })
    });"""
    code = code.replace("ADDRESS1", f"ptr({hex(on_purchase_done.address)})")
    code = code.replace("ADDRESS2", f"ptr({hex(after_purchase.address)})")
    return ref.execute_js(code)


def device_id_cheat():
    ta_util = ref.find_class_in_image("Assembly-CSharp.dll", "TAUtil")
    get_device_id = ta_util.find_method("GetDeviceId")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                ptr(retval).add(0x14).writeU8(0x33);
            }
        })
    });"""
    code = code.replace("ADDRESS", f"ptr({hex(get_device_id.address)})")
    return ref.execute_js(code)


# ???
def blueprint_cheat():
    ItemBluePrint = ref.find_class_in_image("Assembly-CSharp.dll", "ItemBluePrint")
    HasBlueprint = ItemBluePrint.find_method("HasBlueprint")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS2, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                retval.replace(1);
            }
        })
    });"""
    code = code.replace("ADDRESS2", f"ptr({hex(HasBlueprint.address)})")
    return ref.execute_js(code, on_message)


def forge_cheat():
    ui_forge = ref.find_class_in_image("Assembly-CSharp.dll", "UIForge")
    is_unlocked = ui_forge.find_method("IsUnlocked")
    default_weapon_material = ref.find_class_in_image("Assembly-CSharp.dll", "RGWeapon")
    get_materials = default_weapon_material.find_method("GetMaterials")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS1, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                retval.replace(1);
            }
        })
    
        Interceptor.attach(ADDRESS2, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                var cnt = retval.add(0x20).readU32();
                if (cnt <= 5) {
                    var values = retval.add(0x18).readPointer();
                    for (let i = 0; i < cnt; i++) {
                        values.add(0x30 + i * 0x18).writeU8(0);
                    }
                }
            }
        })
    });"""
    code = code.replace("ADDRESS1", f"ptr({hex(is_unlocked.address)})")
    code = code.replace("ADDRESS2", f"ptr({hex(get_materials.address)})")
    return ref.execute_js(code)


def back_cheat():
    rg_hand = ref.find_class_in_image("Assembly-CSharp.dll", "RGHand")
    is_back_full = rg_hand.find_method("IsBackFull")

    code = """
    Java.perform(function () {
        Interceptor.attach(ADDRESS, {
            onEnter: function(args) { },
            onLeave: function(retval) {
                retval.replace(0);
            }
        })
    });"""
    code = code.replace("ADDRESS", f"ptr({hex(is_back_full.address)})")
    return ref.execute_js(code, on_message)


def switch(key: str, ctl: str, func):
    global scripts
    if ctl == "on":
        if key in scripts:
            scripts[key].unload()
        scripts[key] = func()
    elif ctl == "off":
        if key in scripts:
            scripts[key].unload()
            del scripts[key]


while True:
    try:
        cmd_list = input("> ").split(' ')
        cmd = cmd_list[0]
    except:
        continue

    if cmd == "gem":
        switch("gem", cmd_list[1], gem_cheat)
    elif cmd == "fish":
        switch("fish", cmd_list[1], fish_cheat)
    elif cmd == "skill":
        switch("skill", cmd_list[1], skill_cd_cheat)
    elif cmd == "energy":
        switch("energy", cmd_list[1], energy_cheat)
    elif cmd == "armor":
        switch("armor", cmd_list[1], armor_cheat)
    elif cmd == "pay":
        switch("pay", cmd_list[1], pay_cheat)
    elif cmd == "forge":
        switch("forge", cmd_list[1], forge_cheat)
    elif cmd == "back":
        switch("back", cmd_list[1], back_cheat)
    elif cmd == "season_coin":
        season_coin_cheat()
    elif cmd == "list":
        for k in scripts:
            print(k)
    elif cmd == "load":
        with open("1.js") as f:
            ref.execute_js(f.read(), on_message)
    elif cmd == "exit":
        break
