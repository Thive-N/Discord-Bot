import Discord from "discord.js";
import { SlashCommandBuilder } from "@discordjs/builders";

export async function ping(bot: Discord.Client, message: Discord.Message, args: [string]) {
  let pingEmbed = new Discord.MessageEmbed();
  const m = await message.channel.send("Ping?");
  pingEmbed.addField(`Bot Latency is `, `${m.createdTimestamp - message.createdTimestamp}ms.`);
  pingEmbed.addField(`API Latency is `, `${Math.round(bot.ws.ping)}ms`);
  m.edit({ embeds: [pingEmbed] });
}

export const slash = {
  data: new SlashCommandBuilder().setName("ping").setDescription("Replies with Pong!"),
  async execute(interaction: any) {
    await interaction.reply("Pong!");
  },
};

export const help = {
  slash: true,
  name: "ping",
  description: "a ping command to find the response times of the bot",
};
