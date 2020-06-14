package commands;

import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.MessageChannel;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class Quote extends ListenerAdapter {

    private final String QUOTES_URL = "https://type.fit/api/quotes";

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        OkHttpClient client = new OkHttpClient();
        Message message = event.getMessage();

        if (message.getContentRaw().equals("!quote")) {
            try {
                Request request = new Request.Builder()
                        .url(QUOTES_URL)
                        .addHeader("Accept", "application/json")
                        .addHeader("Content-Type", "application/json")
                        .build();

                Response response = client.newCall(request).execute();
                String strJson = response.body().string();

                HashMap<String, String> quote = this.getRandomQuote(strJson);
                this.sendEmbed(quote, event);

            } catch (IOException e) {
                this.handleError(event);
            }
        }
    }

    private HashMap<String, String> getRandomQuote(String json) {
        JSONArray jsonArray = new JSONArray(json);

        Random rand = new Random();
        int randomIndex = rand.nextInt(jsonArray.length());

        JSONObject phrase = jsonArray.getJSONObject(randomIndex);

        HashMap<String, String> quote = new HashMap<>();
        quote.put("text", phrase.getString("text"));
        quote.put("author", phrase.getString("author"));

        return quote;
    }

    private void sendEmbed(HashMap<String, String> quote, MessageReceivedEvent event) {
        EmbedBuilder embed = new EmbedBuilder();
        embed.setTitle(quote.get("text"));
        embed.setDescription(quote.get("author"));

        MessageChannel channel = event.getChannel();
        channel.sendTyping().completeAfter(1, TimeUnit.SECONDS);
        channel.sendMessage(embed.build()).queue();
        embed.clear();
    }

    private void handleError(MessageReceivedEvent event) {
        MessageChannel channel = event.getChannel();
        channel.sendTyping().completeAfter(2, TimeUnit.SECONDS);
        channel.sendMessage("Today's defeat will be greater tomorrow, don't worry. ☺").queue();
    }
}
