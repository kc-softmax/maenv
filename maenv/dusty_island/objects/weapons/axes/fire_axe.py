# import maenv.utils.colors as colors
# from maenv.dusty_island.objects.weapons.magic import MagicWeapon
# from maenv.dusty_island.consts.artifact import (
#     SHOTGUN_BULLET_COUNT,
#     BUSTER_CALL_BOMB_COUNT,
#     BUSTER_CALL_BOMB_RADIUS,
#     BUSTER_CALL_SPAWN_DELAY,
#     ArtifactType
# )
# from maenv.dusty_island.consts.weapons.magic_weapons import (
#     MAGIC_GUN_COOLDOWN,
# )
# from maenv.dusty_island.objects.bullets import Bullet
# from maenv.dusty_island.objects.bombs.poison_bomb import PoisionBomb
# from maenv.dusty_island.objects.bombs.fire_bomb import FireBomb


# class MagicGun(MagicWeapon):

#     render_color = colors.CRIMSON
#     cooldown_duration = MAGIC_GUN_COOLDOWN
#     equippable_artifacts_type = [
#         ArtifactType.SHOTGUN, ArtifactType.POISON_BOMB, ArtifactType.BUSTER_CALL
#     ]

#     def __init__(
#         self,
#     ) -> None:
#         super(MagicGun, self).__init__()

#     def activate_artifact(self) -> list[Bullet]:
#         match self.artifact.artifact_type:
#             case ArtifactType.SHOTGUN:
#                 bullets: list[Bullet] = []
#                 bullet_direction = self.direction.rotate(
#                     False, SHOTGUN_BULLET_COUNT // 2)
#                 for _ in range(SHOTGUN_BULLET_COUNT):
#                     bullet = Bullet(self.center, self.short_id)
#                     bullet.update_direction(bullet_direction)
#                     bullet_direction = bullet_direction.rotate(True)
#                     bullets.append(bullet)
#                 return bullets
#             case ArtifactType.POISON_BOMB:
#                 posion_bomb = PoisionBomb(
#                     self.center, self.short_id, 0.5, self.direction.current_direction)
#                 return [
#                     posion_bomb
#                 ]
#             case ArtifactType.BUSTER_CALL:
#                 fire_bombs = []
#                 for _ in range(BUSTER_CALL_BOMB_COUNT):
#                     fire_bomb = FireBomb(
#                         self.center, self.short_id, 0.5, self.direction.current_direction)
#                     fire_bomb.spawn_radius = BUSTER_CALL_BOMB_RADIUS
#                     fire_bomb.set_delay(
#                         0, BUSTER_CALL_SPAWN_DELAY, True)
#                     fire_bombs.append(fire_bomb)
#                 return fire_bombs
