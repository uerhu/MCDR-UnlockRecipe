from mcdreforged.api.types import PluginServerInterface, InfoCommandSource
from mcdreforged.api.rtext import RTextMCDRTranslation, RTextList, RText, RAction
from mcdreforged.api.command import Literal
from mcdreforged.minecraft.rtext.style import RColor

DEFAULT_CONFIG = {
    "permission": 1,
    "announce": True,
    "announce_once": True
}


class UnlockRecipe:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.config = DEFAULT_CONFIG.copy()
        self.announced_players = list()

    def load_config(self):
        self.config = self.server.load_config_simple(default_config=DEFAULT_CONFIG)

    def register_help_command(self):
        self.server.register_help_message(
            "!!recipe",
            RTextMCDRTranslation("unlock_recipe.help")
        )

    def register_command(self):
        self.server.register_command(
            Literal("!!recipe")
            .runs(lambda src: self.unlock(src))
        )

    def unlock(self, src: InfoCommandSource):
        if src.is_player:
            player = src.get_info().player
            if src.has_permission(int(self.config["permission"])):
                self.server.execute(f"recipe give {player} *")
                self.server.tell(player, RTextMCDRTranslation("unlock_recipe.success.tell").set_color(RColor.green))
                self.server.logger.info(RTextMCDRTranslation("unlock_recipe.success.log", player))
            else:
                self.server.logger.info(RTextMCDRTranslation("unlock_recipe.no_permission.log", player))
                self.server.tell(player,
                                 RTextMCDRTranslation("unlock_recipe.no_permission.tell").set_color(RColor.red))
        else:
            self.server.logger.error(RTextMCDRTranslation("unlock_recipe.no_player"))

    def register_event(self):
        if self.config["announce"]:
            self.server.register_event_listener(
                "mcdr.player_joined",
                self.on_player_joined
            )

    @staticmethod
    def build_announcement():
        announcement = RTextList(
            RTextMCDRTranslation("unlock_recipe.announce.prefix"),
            RText(
                "!!recipe", color=RColor.gray
            )
            .h(RTextMCDRTranslation("unlock_recipe.announce.hover"))
            .c(RAction.run_command, '!!recipe'),
            RTextMCDRTranslation("unlock_recipe.announce.suffix")
        )
        return announcement

    def load_announced_players(self):
        if self.config["announce"] and self.config["announce_once"]:
            self.announced_players = self.server.load_config_simple(
                "announced_players.json",
                default_config={
                    "announced_players": []
                }
            ).get("announced_players", [])

    def save_announced_players(self):
        if self.config["announce"] and self.config["announce_once"]:
            self.server.save_config_simple({
                "announced_players": self.announced_players
            },
                "announced_players.json"
            )

    def on_player_joined(self, server: PluginServerInterface, player: str, _):
        if not self.config["announce"]:
            return
        if self.config["announce_once"] and player in self.announced_players:
            return
        server.tell(player, self.build_announcement())
        self.announced_players.append(player)
        self.save_announced_players()


def on_load(server: PluginServerInterface, _):
    unlocker = UnlockRecipe(server)
    unlocker.load_config()
    unlocker.load_announced_players()
    unlocker.register_help_command()
    unlocker.register_command()
    unlocker.register_event()
