package discord;

import commands.Help;
import commands.Quote;
import enums.BotListeningActivity;
import enums.BotPlayingActivity;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.entities.Activity;

import javax.security.auth.login.LoginException;

public class PotatoBot {
    private JDA jda;

    public PotatoBot(String token) {
        try {
            this.jda = JDABuilder.createDefault(token).build();
            this.jda.getPresence().setStatus(OnlineStatus.IDLE);
            this.setPlayingActivity(BotPlayingActivity.IM_DEPRESSED);
            this.jda.addEventListener(new Help());
            this.jda.addEventListener(new Quote());
        } catch (LoginException e) {
            System.out.println("Error authenticating Potato bot with discord.");
            System.exit(1);
        }
    }

    public void setPlayingActivity(BotPlayingActivity playingActivity) {
        this.jda.getPresence().setActivity(Activity.playing(playingActivity.value()));
    }

    public void setListeningActivity(BotListeningActivity listeningActivity) {
        this.jda.getPresence().setActivity(Activity.listening(listeningActivity.value()));
    }
}
