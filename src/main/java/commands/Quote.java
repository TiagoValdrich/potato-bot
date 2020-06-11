package commands;

import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.MessageChannel;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

import static java.net.HttpURLConnection.HTTP_OK;

public class Quote extends ListenerAdapter {

    private final String QUOTES_URL = "https://type.fit/api/quotes";

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        Message message = event.getMessage();

        if (message.getContentRaw().equals("!quote")) {
            try {
                URL url = new URL(QUOTES_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();

                conn.setRequestMethod("GET");
                conn.setRequestProperty("Accept", "application/json");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.connect();

                int responseCode = conn.getResponseCode();

                if (responseCode == HTTP_OK) {
                    Scanner sc = new Scanner(url.openStream());
                    String strJSON = "";

                    while (sc.hasNext()) {
                        strJSON += sc.nextLine();
                    }

                    JSONArray jarray = new JSONArray(strJSON);
                    Random rand = new Random();
                    int randomIndex = rand.nextInt(jarray.length());

                    JSONObject phrase = jarray.getJSONObject(randomIndex);
                    String text = phrase.getString("text");
                    String author = phrase.getString("author");

                    EmbedBuilder embed = new EmbedBuilder();
                    embed.setTitle(text);
                    embed.setDescription(author);

                    MessageChannel channel = event.getChannel();
                    channel.sendTyping().completeAfter(1, TimeUnit.SECONDS);
                    channel.sendMessage(embed.build()).queue();
                    embed.clear();

                } else {
                    throw new Exception("Error on fetching quotes");
                }
            } catch (MalformedURLException e) {
                this.handleError(event);
            } catch (IOException e) {
                this.handleError(event);
            } catch (Exception e) {
                this.handleError(event);
            }
        }
    }

    private void handleError(MessageReceivedEvent event) {
        MessageChannel channel = event.getChannel();
        channel.sendTyping().completeAfter(2, TimeUnit.SECONDS);
        channel.sendMessage("Today's defeat will be greater tomorrow, don't worry. ☺").queue();
    }
}
