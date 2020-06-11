package commands;

import net.dv8tion.jda.api.EmbedBuilder;
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
            EmbedBuilder embed = new EmbedBuilder();

            embed.setColor(0xeb4034);
            embed.setTitle("Potato Bot - Command list");
            embed.addField("!help", "Hey, you are using this command!", false);
            embed.addField("!quote", "Show a nice random quote", false);

            MessageChannel channel = event.getChannel();
            channel.sendMessage(embed.build()).queue();
            embed.clear();
        }
    }
}
