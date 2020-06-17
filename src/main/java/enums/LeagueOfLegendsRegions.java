package enums;

public enum LeagueOfLegendsRegions {
    BR("br1"),
    EUN("en1"),
    EUW("euw1"),
    JP("jp1"),
    KR("kr"),
    LAN("la1"),
    LAS("la2"),
    NA("na1"),
    OC("oc1"),
    TR("tr1"),
    RU("ru");

    private String value;

    LeagueOfLegendsRegions(String value) { this.value = value; }

    public String value() {
        return this.value;
    }
}
