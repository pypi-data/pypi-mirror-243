from .build_serials import Serial

republic_act = Serial(
    duo="ra",
    regex="\\d{1,5}",
    variants=[
        "republic act",
        "rep act,",
        "rep. act",
    ],
)

commonwealth_act = Serial(
    duo="ca",
    regex="\\d{1,3}",
    variants=[
        "commonwealth act",
        "com act",
        "com. act",
    ],
)

batas_pambansa = Serial(
    duo="bp",
    regex="\\d{1,3}(-?(A|B))?",
    variants=[
        "batas pambansa",
    ],
    pre=["Blg."],
)

executive_order = Serial(
    duo="eo",
    regex="\\d{1,4}(-?(A|B|C))?",
    variants=[
        "executive order",
        "exec order",
        "exec. order",
    ],
)

pres_decree = Serial(
    duo="pd",
    regex="\\d{1,4}(-?(A|B))?",
    variants=[
        "presidential decree",
        "pres decree",
        "pres dec.",
        "pres. decree",
        "pres. dec.",
    ],
)

act = Serial(
    regex="\\d{1,4}",
    variants=["act"],
)

patterns_statute = (
    republic_act.patterns
    + pres_decree.patterns
    + commonwealth_act.patterns
    + batas_pambansa.patterns
    + act.patterns
    + executive_order.patterns
)
