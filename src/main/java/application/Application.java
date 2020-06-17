package application;

import discord.PotatoBot;

public class Application {
    public static void main(String args[]) {
        try {
            String token = System.getenv("POTATO_BOT_SECRETS");
            PotatoBot potatoBot = new PotatoBot(token);
        } catch (Exception e) {
            System.out.println("Error on bot startup: " + e);
        }
    }
}
