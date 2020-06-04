package commands;

import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.MessageChannel;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class Help extends ListenerAdapter {
    public void onMessageReceived(MessageReceivedEvent event)
    {
        Message msg = event.getMessage();
        if (msg.getContentRaw().equals("!help"))
        {
            String author = event.getAuthor().getName();
            String responseMessage = "Hello " + author +
                    ", how are you? Currently only !help exists, i'm too depressed to develop more commands xD.";
            MessageChannel channel = event.getChannel();
            channel.sendMessage(responseMessage).queue();
        }
    }
}
