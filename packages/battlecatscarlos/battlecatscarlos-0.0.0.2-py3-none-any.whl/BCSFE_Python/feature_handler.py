"""Handler for selecting and running editor features"""

from typing import Any, Union

from . import (
    helper,
    user_input_handler,
    config_manager,
)
from .edits import basic, cats, gamototo, levels, other, save_management


def fix_elsewhere_old(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Fix the elsewhere error using 2 save files"""

    main_token = save_stats["token"]
    main_iq = save_stats["inquiry_code"]
    input(
        "Select a save file that is currently loaded in-game that doesn't have the elsehere error and is not banned\nPress enter to continue:"
    )
    new_path = helper.select_file(
        "Select a clean save file",
        helper.get_save_file_filetype(),
        helper.get_save_path(),
    )
    if not new_path:
        print("Please select a save file")
        return save_stats

    data = helper.load_save_file(new_path)
    new_stats = data["save_stats"]
    new_token = new_stats["token"]
    new_iq = new_stats["inquiry_code"]
    save_stats["token"] = new_token
    save_stats["inquiry_code"] = new_iq

    helper.colored_text(f"Replaced inquiry code: &{main_iq}& with &{new_iq}&")
    helper.colored_text(f"Replaced token: &{main_token}& with &{new_token}&")
    return save_stats


FEATURES: dict[str, Any] = {
    "資料處理": {
        "儲存本機檔案": save_management.save.save_save,
        "上傳到伺服器": save_management.server_upload.save_and_upload,
        "儲存": save_management.save.save,
        "Save changes and push save data to the game with adb (don't re-open game)": save_management.save.save_and_push,
        "Save changes and push save data to the game with adb (re-open game)": save_management.save.save_and_push_rerun,
        "Export save data as json": save_management.other.export,
        "Clear save data with adb (used to generate a new account without re-installing the game)": save_management.other.clear_data,
        "Upload tracked bannable items (This is done automatically when saving or exiting)": save_management.server_upload.upload_metadata,
        "載入資料": save_management.load.select,
        "版本轉換": save_management.convert.convert_save,
        # "Manage Presets": preset_handler.preset_manager,
    },
    "道具": {
        "罐頭": basic.basic_items.edit_cat_food,
        "XP": basic.basic_items.edit_xp,
        "卷": {
            "銀卷": basic.basic_items.edit_normal_tickets,
            "金卷": basic.basic_items.edit_rare_tickets,
            "白金卷": basic.basic_items.edit_platinum_tickets,
            "白金碎片": basic.basic_items.edit_platinum_shards,
            "傳説卷": basic.basic_items.edit_legend_tickets,
        },
        "NP": basic.basic_items.edit_np,
        "首領旗": basic.basic_items.edit_leadership,
        "戰鬥道具": basic.basic_items.edit_battle_items,
        "貓眼石": basic.catseyes.edit_catseyes,
        "貓薄荷 / 獸石": basic.catfruit.edit_catfruit,
        "本能珠": basic.talent_orbs_new.edit_talent_orbs,
        "貓力達": basic.basic_items.edit_catamins,
        "任務取得（新功能）": other.scheme_item.edit_scheme_data,
    },
    "加碼多多": {
        "Ototo Engineers": basic.basic_items.edit_engineers,
        "Base materials": basic.ototo_base_mats.edit_base_mats,
        "Catamins": basic.basic_items.edit_catamins,
        "Gamatoto XP / Level": gamototo.gamatoto_xp.edit_gamatoto_xp,
        "Ototo Cat Cannon": gamototo.ototo_cat_cannon.edit_cat_cannon,
        "Gamatoto Helpers": gamototo.helpers.edit_helpers,
        "Fix gamatoto from crashing the game": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "Cats / Special Skills": {
        "Get / Remove Cats": {
            "Get Cats": cats.get_remove_cats.get_cat,
            "Remove Cats": cats.get_remove_cats.remove_cats,
        },
        "Upgrade Cats": cats.upgrade_cats.upgrade_cats,
        "True Form Cats": {
            "Get Cat True Forms": cats.evolve_cats.get_evolve,
            "Remove Cat True Forms": cats.evolve_cats.remove_evolve,
            "Force True Form Cats (will lead to blank cats for cats without a true form)": cats.evolve_cats.get_evolve_forced,
        },
        "Talents": {
            "Set talents for each selected cat individually": cats.talents.edit_talents_individual,
            "Max / Remove all selected cat talents": cats.talents.max_all_talents,
        },
        "Collect / Remove Cat Guide": {
            "Set Cat Guide Entries (does not give cf)": cats.clear_cat_guide.collect_cat_guide,
            "Unclaim Cat Guide Entries": cats.clear_cat_guide.remove_cat_guide,
        },
        'Get stage unit drops - removes the "Clear this stage to get special cat" dialog': cats.chara_drop.get_character_drops,
        "Upgrade special skills / abilities": cats.upgrade_blue.upgrade_blue,
    },
    "關卡": {
        "主世界": {
            "一次通關所有章節": levels.main_story.clear_all,
            "通過一個章節的關卡": levels.main_story.clear_each,
        },
        "寶物": {
            "寶物組 (e.g energy drink, aqua crystal, etc)": levels.treasures.treasure_groups,
            "Specific stages and specific chapters individually": levels.treasures.specific_stages,
            "所有關卡一次來": levels.treasures.specific_stages_all_chapters,
        },
        "不死 / Outbreaks": levels.outbreaks.edit_outbreaks,
        "Event Stages": levels.event_stages.event_stages,
        "舊傳奇": levels.event_stages.stories_of_legend,
        "新傳奇": levels.uncanny.edit_uncanny,
        "Aku Realm/Gates Clearing": levels.aku.edit_aku,
        "Unlock the Aku Realm/Gates": levels.unlock_aku_realm.unlock_aku_realm,
        "Gauntlets": levels.gauntlet.edit_gauntlet,
        "Collab Gauntlets": levels.gauntlet.edit_collab_gauntlet,
        "風雲塔": levels.towers.edit_tower,
        "Behemoth Culling": levels.behemoth_culling.edit_behemoth_culling,
        "未來分數": levels.itf_timed_scores.timed_scores,
        "挑戰賽分數": basic.basic_items.edit_challenge_battle,
        "清除教學": levels.clear_tutorial.clear_tutorial,
        "Catclaw Dojo Score (Hall of Initiates)": basic.basic_items.edit_dojo_score,
        "Add Enigma Stages": levels.enigma_stages.edit_enigma_stages,
        "Allow the filibuster stage to be recleared": levels.allow_filibuster_clearing.allow_filibuster_clearing,
        "Legend Quest": levels.legend_quest.edit_legend_quest,
    },
    "賬號": {
        "詢問碼": basic.basic_items.edit_inquiry_code,
        "Token": basic.basic_items.edit_token,
        "Fix elsewhere error / Unban account": other.fix_elsewhere.fix_elsewhere,
        "Old Fix elsewhere error / Unban account (needs 2 save files)": fix_elsewhere_old,
        "Generate a new inquiry code and token": other.create_new_account.create_new_account,
    },
    "其他": {
        "Rare Gacha Seed": basic.basic_items.edit_rare_gacha_seed,
        "Unlocked Equip Slots": basic.basic_items.edit_unlocked_slots,
        "初心者禮包": basic.basic_items.edit_restart_pack,
        "Meow Medals": other.meow_medals.medals,
        "Play Time": other.play_time.edit_play_time,
        "Unlock / Remove Enemy Guide Entries": other.unlock_enemy_guide.enemy_guide,
        "Catnip Challenges / Missions": other.missions.edit_missions,
        "藍珠金卷": other.trade_progress.set_trade_progress,
        "王金會員": other.get_gold_pass.get_gold_pass,
        "Claim / Remove all user rank rewards (does not give any items)": other.claim_user_rank_rewards.edit_rewards,
        "Cat Shrine Level / XP": other.cat_shrine.edit_shrine_xp,
    },
    "Fixes": {
        "Fix time errors": other.fix_time_issues.fix_time_issues,
        "Unlock the Equip Menu": other.unlock_equip_menu.unlock_equip,
        "Clear Tutorial": levels.clear_tutorial.clear_tutorial,
        "Fix elsewhere error / Unban account": other.fix_elsewhere.fix_elsewhere,
        "Old Fix elsewhere error / Unban account (needs 2 save files)": fix_elsewhere_old,
        "Fix gamatoto from crashing the game": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "Edit Config": {
        "Edit LOCALIZATION": config_manager.edit_locale,
        "Edit DEFAULT_COUNTRY_CODE": config_manager.edit_default_gv,
        "Edit DEFAULT_SAVE_PATH": config_manager.edit_default_save_file_path,
        "Edit FIXED_SAVE_PATH": config_manager.edit_fixed_save_path,
        "Edit EDITOR settings": config_manager.edit_editor_settings,
        "Edit START_UP settings": config_manager.edit_start_up_settings,
        "Edit SAVE_CHANGES settings": config_manager.edit_save_changes_settings,
        "Edit SERVER settings": config_manager.edit_server_settings,
        "Edit config path": config_manager.edit_config_path,
    },
    "退出": helper.exit_check_changes,
}


def get_feature(
    selected_features: Any, search_string: str, results: dict[str, Any]
) -> dict[str, Any]:
    """Search for a feature if the feature name contains the search string"""

    for feature in selected_features:
        feature_data = selected_features[feature]
        if isinstance(feature_data, dict):
            feature_data = get_feature(feature_data, search_string, results)
        if search_string.lower().replace(" ", "") in feature.lower().replace(" ", ""):
            results[feature] = selected_features[feature]
    return results


def show_options(
    save_stats: dict[str, Any], features_to_use: dict[str, Any]
) -> dict[str, Any]:
    """Allow the user to either enter a feature number or a feature name, and get the features that match"""

    if (
        not config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES")
        and FEATURES == features_to_use
    ):
        user_input = ""
    else:
        prompt = (
            "What do you want to edit (some options contain other features within them)"
        )
        if config_manager.get_config_value_category(
            "EDITOR", "SHOW_FEATURE_SELECT_EXPLANATION"
        ):
            prompt += "\nYou can enter a number to run a feature or a word to search for that feature (e.g entering catfood will run the Cat Food feature, and entering tickets will show you all the features that edit tickets)\nYou can press enter to see a list of all of the features"
        user_input = user_input_handler.colored_input(f"{prompt}:\n")
    user_int = helper.check_int(user_input)
    results = []
    if user_int is None:
        results = get_feature(features_to_use, user_input, {})
    else:
        if user_int < 1 or user_int > len(features_to_use) + 1:
            helper.colored_text("Value out of range", helper.RED)
            return show_options(save_stats, features_to_use)
        if FEATURES != features_to_use:
            if user_int - 2 < 0:
                return menu(save_stats)
            results = features_to_use[list(features_to_use)[user_int - 2]]
        else:
            results = features_to_use[list(features_to_use)[user_int - 1]]
    if not isinstance(results, dict):
        save_stats_return = results(save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return
    if len(results) == 0:
        helper.colored_text("No feature found with that name.", helper.RED)
        return menu(save_stats)
    if len(results) == 1 and isinstance(list(results.values())[0], dict):
        results = results[list(results)[0]]
    if len(results) == 1:
        save_stats_return = results[list(results)[0]](save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return

    helper.colored_list(["Go Back"] + list(results))
    return show_options(save_stats, results)


def menu(
    save_stats: dict[str, Any], path_save: Union[str, None] = None
) -> dict[str, Any]:
    """Show the menu and allow the user to select a feature to edit"""

    if path_save:
        helper.set_save_path(path_save)
    if config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES"):
        helper.colored_list(list(FEATURES))
    save_stats = show_options(save_stats, FEATURES)

    return save_stats
