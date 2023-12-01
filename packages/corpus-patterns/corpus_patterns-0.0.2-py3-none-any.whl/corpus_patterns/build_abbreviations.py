from collections.abc import Iterator
from enum import Enum
from typing import NamedTuple

from .utils import TitledString


class Def(NamedTuple):
    """A (possible) definition of a commonly used abbreviation;
    each value must be a `TitledString` so that it can be
    adjusted for lowercase / uppercase variants."""

    title: TitledString
    abbv: TitledString | None = None

    @staticmethod
    def get_cased_value(v: str, cased: str | None = None) -> str:
        if cased:
            if cased == "lower":
                return v.lower()
            elif cased == "upper":
                return v.upper()
        return v

    @property
    def dotted_abbv(self) -> list[str]:
        bits = []
        if self.abbv:
            for style in (None, "lower", "upper"):
                bits.append(self.get_cased_value(self.abbv, cased=style))
                bits.append(self.get_cased_value(self.abbv + ".", cased=style))
        return bits

    @property
    def options(self) -> list[str]:
        bits = []
        for style in (None, "lower", "upper"):
            bits.append(self.get_cased_value(self.title, cased=style))
        return bits + self.dotted_abbv


class Abbv(Enum):
    """Some common abbreviations used in Philippine legal text."""

    Adm = Def(title="Administrative", abbv="Adm")
    Admin = Def(title="Administrative", abbv="Admin")
    Pres = Def(title="Presidential", abbv="Pres")
    Dec = Def(title="Decree", abbv="Dec")
    Executive = Def(title="Executive", abbv="Exec")
    Blg = Def(title="Bilang", abbv="Blg")
    Number = Def(title="Number", abbv="No")
    Numbers = Def(title="Numbers", abbv="Nos")
    Const = Def(title="Constitution", abbv="Const")
    Company = Def(title="Company", abbv="Co")
    Corporation = Def(title="Corporation", abbv="Corp")
    Incorporated = Def(title="Incorporated", abbv="Inc")
    Phil1 = Def(title="Philippines", abbv="Phil")
    Phil2 = Def(title="Philippines", abbv="Phils")
    Limited = Def(title="Limited", abbv="Ltd")
    Association = Def(title="Association", abbv="Assoc")
    Assistant = Def(title="Assistant", abbv="Ass")
    Department = Def(title="Department", abbv="Dept")
    Nat1 = Def(title="National", abbv="Nat")
    Nat2 = Def(title="National", abbv="Natl")
    St = Def(title="Street", abbv="St")
    Road = Def(title="Road", abbv="Rd")
    Ave = Def(title="Avenue", abbv="Ave")
    Blk = Def(title="Block", abbv="Blk")
    Brgy = Def(title="Barangay", abbv="Brgy")
    Building = Def(title="Building", abbv="Bldg")
    Purok = Def(title="Purok", abbv="Prk")
    Subdivision = Def(title="Subdivision", abbv="Subd")
    Highway = Def(title="Highway", abbv="Hwy")
    Municipality = Def(title="Municipality", abbv="Mun")
    City = Def(title="City", abbv="Cty")
    Province = Def(title="Province", abbv="Prov")
    Governor = Def(title="Governor", abbv="Gov")
    Congressman = Def(title="Congressman", abbv="Cong")
    General = Def(title="General", abbv="Gen")
    Lieutenant = Def(title="Lieutenant", abbv="Lt")
    Sct = Def(title="Scout", abbv="Sct")
    Sta = Def(title="Santa", abbv="Sta")
    Sto = Def(title="Santo", abbv="Sto")
    Vda = Def(title="Viuda", abbv="Vda")
    Jr = Def(title="Junior", abbv="Jr")
    Sr = Def(title="Senior", abbv="Sr")
    Fr = Def(title="Father", abbv="Fr")
    Bro = Def(title="Brother", abbv="Bro")
    Dr = Def(title="Doctor", abbv="Dr")
    Dra = Def(title="Doctora", abbv="Dra")
    Maria = Def(title="Maria", abbv="Ma")
    Hon = Def(title="Honorable", abbv="Hon")
    Atty = Def(title="Attorney", abbv="Atty")
    Engr = Def(title="Engineer", abbv="Engr")
    Justice = Def(title="Justice", abbv="J")
    January = Def(title="January", abbv="Jan")
    February = Def(title="February", abbv="Feb")
    March = Def(title="March", abbv="Mar")
    April = Def(title="April", abbv="Apr")
    May = Def(title="May")
    June = Def(title="June", abbv="Jun")
    July = Def(title="July", abbv="Jul")
    August = Def(title="August", abbv="Aug")
    Sept1 = Def(title="September", abbv="Sept")
    Sept2 = Def(title="September", abbv="Sep")
    October = Def(title="October", abbv="Oct")
    November = Def(title="November", abbv="Nov")
    December = Def(title="December", abbv="Dec")

    @classmethod
    def set_abbvs(cls, cased: str | None = None) -> Iterator[str]:
        for member in cls:
            if v := member.value.abbv:
                yield Def.get_cased_value(v, cased)

    @classmethod
    def set_fulls(cls, cased: str | None = None) -> Iterator[str]:
        for member in cls:
            yield Def.get_cased_value(member.value.title, cased)
