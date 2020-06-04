package discord;

import commands.Help;
import enums.BotListeningActivity;
import enums.BotPlayingActivity;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.entities.Activity;

import javax.security.auth.login.LoginException;

public class PotatoBot {
    private JDA jda;

    public PotatoBot() {
        try {
            this.jda = JDABuilder.createDefault("NzE3MTU3MDIzODM3MzIzMzc2.Xtgcnw.2C0F1p4wDoaJ9dtjNAbdWG143Fc").build();
            this.jda.getPresence().setStatus(OnlineStatus.IDLE);
            this.setPlayingActivity(BotPlayingActivity.IM_DEPRESSED);
            this.jda.addEventListener(new Help());
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
