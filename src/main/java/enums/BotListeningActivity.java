package enums;

public enum BotListeningActivity {
    DEPRESSION("depression | type !help for more info"),
    THE_VOICE_OF_DEATH("the voice of death | type !help for more info");

    private String description;

    BotListeningActivity(String value) {
        this.description = value;
    }

    public String value() {
        return this.description;
    }
}
