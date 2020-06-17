package commands;

import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class SearchLolPlayer extends ListenerAdapter {
    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        Message message = event.getMessage();
        String arguments[] = message.toString().split(" ");

        if (arguments[0].equalsIgnoreCase("!searchlolplayer")) {
            // @TODO: Create this command :D
        }
    }
}
