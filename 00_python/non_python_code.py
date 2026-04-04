def make_chai():
    if notkettle_has_water():
        fill_kettle()
    plug_in_kettle()
    boil_water()
    if not is_cup_clean():
        wash_cup()
    add_to_cup("tea_leaves")
    add_to_cup("sugar")
    pour("boiled_water")
    stie("cup")
    serve("chai")

make_chai()