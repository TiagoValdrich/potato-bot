package enums;

public enum BotPlayingActivity {
    WITH_DEPRESSION("with depression | type !help for more info"),
    WITH_LIFE("with the life | type !help for more info"),
    IM_DEPRESSED("to com depressaum | type !help for more info");

    private String description;

    BotPlayingActivity(String value) {
        this.description = value;
    }

    public String value() {
        return this.description;
    }
}
