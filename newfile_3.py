# ================================================================================
#  📱 HUNTER MAFIA — WEB O'YIN (3-QISM)
#
#  Bu fayl 1-qism (newfile.py) va 2-qism (hunter_mafia_new.py) bilan BIR XIL global
#  nomlar maydonida bajariladi (exec). Alohida o'yin dvigateli YO'Q: web o'yin
#  klassik /game bilan BIR XIL dvigateldan (GAMES, start_night, resolve_night, ...)
#  foydalanadi. Farqi faqat o'yinchi interfeysida:
#
#   • web o'yinchilarga ketadigan shaxsiy xabarlar (matn + inline tugmalar) Telegramga
#     yuborilmaydi — ilovadagi "so'rov" (prompt) kartalariga aylanadi;
#   • ilovada tugma bosilganda aynan o'sha eski callback ishlovchisi chaqiriladi
#     (shuning uchun BARCHA rollar qo'shimcha kodsiz ishlaydi);
#   • guruhga ketadigan voqea xabarlari "o'yin lentasi"ga yig'iladi, guruhga esa
#     faqat qisqa xabarlar ketadi (boshlandi / tun / tong / ovoz natijasi / g'oliblar);
#   • 🎙 Ovozli boshlovchi: owner botda yuklagan mp3/m4a lar o'yin voqealarida o'ynaydi.
#
#  Fayl nomlari: webgame.html (sahifa) — bot uni /wg manzilidan beradi.
# ================================================================================
import itertools as _wg_it
import hashlib as _wg_hashlib
import mimetypes as _wg_mimetypes
from types import SimpleNamespace as _NS
from collections import OrderedDict as _OD

WG_VERSION = 1
WG_MAX_DEFAULT = 30
WG_LOBBY_SECONDS_DEFAULT = 150
WG_LOBBY_HARDCAP = 3 * 3600   # admin boshlamasa, lobbi 3 soatdan keyin yopiladi (avto-boshlash YO'Q)
WG_T_DEFAULT = {"night": 40, "discuss": 90, "vote": 40, "confirm": 20}
WG_FEED_MAX = 600
WG_CHAT_MAX = 300
WG_KEEP_AFTER_END = 3600
WG_DM_MAX = 80

_WG_LOCK = threading.RLock()
WGS = {}            # chat_id -> web o'yin holati
WG_UID = {}         # uid -> chat_id (lobbi yoki faol web o'yin)
_WG_MID = _wg_it.count(910_000_000)
_WG_TL = threading.local()
_WG_ORIG = {}
_WG_RATE = {}


def _wg_setting_int(key, default):
    try:
        v = get_setting(key)
        return int(v) if v not in (None, "") else default
    except Exception:
        return default


# ------------------------------------------------------------------------------
#  Jins (Yigit/Qiz) — lobbida tanlanadi, personaj modeli shunga qarab beriladi
# ------------------------------------------------------------------------------
def wg_gender(uid):
    try:
        return "f" if get_setting("wgg_%d" % int(uid)) == "f" else "m"
    except Exception:
        return "m"


def wg_gender_set(uid, gd):
    set_setting("wgg_%d" % int(uid), "f" if gd == "f" else "m")


def wg_times():
    """Web o'yin faza vaqtlari (soniya): tun / muhokama / ovoz berish / tasdiqlash. Owner paneldan o'zgaradi."""
    d = WG_T_DEFAULT
    return {"night": max(15, min(300, _wg_setting_int("wgt_night", d["night"]))),
            "discuss": max(15, min(600, _wg_setting_int("wgt_discuss", d["discuss"]))),
            "vote": max(15, min(300, _wg_setting_int("wgt_vote", d["vote"]))),
            "confirm": d["confirm"]}


def wg_max_players():
    return max(3, _wg_setting_int("wg_max", WG_MAX_DEFAULT))


def wg_lobby_seconds():
    return max(30, _wg_setting_int("wg_lobby_s", WG_LOBBY_SECONDS_DEFAULT))


# ------------------------------------------------------------------------------
#  Yordamchilar
# ------------------------------------------------------------------------------
_WG_TAG_KEEP = re.compile(r"<(?!/?(?:b|i|u|s|code|pre|strong|em)>)[^>]*>", re.I)
_WG_TGEMOJI = re.compile(r"<tg-emoji[^>]*>(.*?)</tg-emoji>", re.I | re.S)


def _wg_clean(txt):
    """Telegram HTML -> xavfsiz oddiy HTML (faqat b/i/u/s/code/pre; boshqa teglar olib tashlanadi)."""
    if txt is None:
        return ""
    t = str(txt)
    t = _WG_TGEMOJI.sub(lambda m: m.group(1), t)
    t = _WG_TAG_KEEP.sub("", t)
    return t[:3500]


def _wg_plain(txt):
    return re.sub(r"<[^>]+>", "", _wg_clean(txt))


def _wg_buttons(markup):
    """InlineKeyboardMarkup -> [[{t, d}]] (faqat callback tugmalar)."""
    rows = []
    if markup is None:
        return rows
    kb = getattr(markup, "keyboard", None)
    if kb is None:
        kb = getattr(markup, "rows", None)
    for row in (kb or []):
        out = []
        for b in row:
            d = getattr(b, "callback_data", None)
            if d is None and isinstance(b, dict):
                d = b.get("callback_data")
            t = getattr(b, "text", None) if not isinstance(b, dict) else b.get("text")
            if d and t is not None:
                out.append({"t": _wg_plain(t), "d": str(d)})
        if out:
            rows.append(out)
    return rows


def _wg_fake_msg(chat_id, text=""):
    return _NS(message_id=next(_WG_MID), chat=_NS(id=chat_id, type=("private" if chat_id > 0 else "supergroup"), title=None),
               text=text, date=int(time.time()), from_user=_NS(id=0, is_bot=True), content_type="text")


def _wg_new_state(chat_id, title, creator):
    return {
        "chat_id": chat_id, "title": title or "Guruh", "creator": creator, "created": time.time(),
        "lobby_end": time.time() + WG_LOBBY_HARDCAP, "extended": 0,
        "feed": [], "fid": 0, "chat": [], "cid": 0, "team": [], "tid": 0, "dead": [], "did": 0,
        "dm": {}, "toast": {}, "ver": 0, "cond": threading.Condition(),
        "ended": False, "ended_ts": 0, "result": None, "starting": False, "started": False,
        "spec": {}, "ann_mid": None, "ann_dirty": True, "ann_ts": 0,
        "voice": [], "vid": 0, "bgm": None, "ready": set(), "last_seen": {},
    }


def _wg_bump(st):
    st["ver"] += 1
    try:
        with st["cond"]:
            st["cond"].notify_all()
    except Exception:
        pass


def _wg_game(chat_id):
    g = GAMES.get(chat_id)
    return g if (g and g.get("web")) else None


# ------------------------------------------------------------------------------
#  Yo'naltirish: bot chaqiruvi web o'yinchiga/web guruhga tegishlimi?
# ------------------------------------------------------------------------------
def _wg_route(chat_id):
    """None | ("dm", uid, st) | ("group", chat_id, st)"""
    if not isinstance(chat_id, int):
        return None
    if chat_id > 0:
        cid = WG_UID.get(chat_id)
        if cid is None:
            return None
        st = WGS.get(cid)
        if not st or st["ended"]:
            return None
        return ("dm", chat_id, st)
    st = WGS.get(chat_id)
    if not st or st["ended"]:
        return None
    g = GAMES.get(chat_id)
    if not g or not g.get("web"):
        return None
    if g.get("phase") == "waiting" and not st.get("starting") and not st.get("started"):
        return None   # lobbi e'loni va boshqa oddiy xabarlar guruhga ketaveradi
    return ("group", chat_id, st)


def _wg_feed_add(st, text, kind="g", scene=None, mid=None, extra=None):
    with _WG_LOCK:
        st["fid"] += 1
        it = {"i": st["fid"], "t": int(time.time()), "k": kind, "x": _wg_clean(text), "mid": mid}
        if scene:
            it["sc"] = scene
        if extra:
            it.update(extra)
        st["feed"].append(it)
        if len(st["feed"]) > WG_FEED_MAX:
            del st["feed"][: len(st["feed"]) - WG_FEED_MAX]
    _wg_bump(st)
    return it


def _wg_dm_put(st, uid, mid, text, markup):
    with _WG_LOCK:
        d = st["dm"].setdefault(uid, _OD())
        btns = _wg_buttons(markup)
        e = d.get(mid)
        if e is None:
            e = {"mid": mid, "ts": time.time(), "n": next(_WG_MID)}
            d[mid] = e
        e["x"] = _wg_clean(text)
        e["b"] = btns
        e["ut"] = time.time()
        while len(d) > WG_DM_MAX:
            d.popitem(last=False)
    _wg_bump(st)


def _wg_toast(st, uid, text, alert=False):
    if not text:
        return
    with _WG_LOCK:
        lst = st["toast"].setdefault(uid, [])
        lst.append({"id": next(_WG_MID), "x": _wg_plain(text)[:300], "a": bool(alert)})
        del lst[:-8]
    _wg_bump(st)


# ------------------------------------------------------------------------------
#  Bot o'rovchilari (send_message va boshqalar)
# ------------------------------------------------------------------------------
def _wg_install_interceptors():
    if globals().get("_WG_INSTALLED"):
        return

    def _orig(name):
        return _WG_ORIG[name]

    for name in ("send_message", "send_photo", "send_animation", "send_video", "send_document", "send_audio",
                 "edit_message_text", "edit_message_caption", "edit_message_reply_markup", "delete_message",
                 "answer_callback_query", "reply_to", "send_chat_action", "pin_chat_message"):
        fn = getattr(bot, name, None)
        if fn is not None:
            _WG_ORIG[name] = fn

    def _record_send(route, text, markup, scene=None):
        mid = next(_WG_MID)
        kind, key, st = route
        if kind == "dm":
            _wg_dm_put(st, key, mid, text, markup)
        else:
            _b = _wg_buttons(markup)
            _wg_feed_add(st, text, "g", scene=scene or getattr(_WG_TL, "scene", None), mid=mid,
                         extra=({"b": _b} if _b else None))
        return mid

    def _mk_send(name, text_arg):
        orig = _WG_ORIG.get(name)
        if orig is None:
            return None

        def w(chat_id, *a, **k):
            route = _wg_route(chat_id)
            if route is None:
                return orig(chat_id, *a, **k)
            text = None
            if text_arg == "text":
                text = k.get("text") if "text" in k else (a[0] if a else "")
            elif text_arg == "caption":
                text = k.get("caption")
            if name == "send_document" or name == "send_audio":
                text = text or ""
            mk = k.get("reply_markup")
            mid = _record_send(route, text or "", mk) if (text or mk) else next(_WG_MID)
            if getattr(_WG_TL, "mode", None) == "both" and route[0] == "group":
                try:
                    orig(chat_id, *a, **k)
                except Exception:
                    pass
            return _NS(message_id=mid, chat=_NS(id=chat_id), text=text, date=int(time.time()))
        w.__name__ = name
        return w

    for name, targ in (("send_message", "text"), ("send_photo", "caption"), ("send_animation", "caption"),
                       ("send_video", "caption"), ("send_document", "caption"), ("send_audio", "caption")):
        w = _mk_send(name, targ)
        if w:
            setattr(bot, name, w)

    # --- reply_to(message, text)
    if "reply_to" in _WG_ORIG:
        _o = _WG_ORIG["reply_to"]

        def reply_to(message, text, *a, **k):
            cid = getattr(getattr(message, "chat", None), "id", None)
            route = _wg_route(cid)
            if route is None:
                return _o(message, text, *a, **k)
            mid = _record_send(route, text, k.get("reply_markup"))
            return _NS(message_id=mid, chat=_NS(id=cid), text=text)
        bot.reply_to = reply_to

    # --- edit_message_text(text, chat_id, message_id, ...)
    def _edit(name, argname):
        orig = _WG_ORIG.get(name)
        if orig is None:
            return None

        def w(*a, **k):
            if name == "edit_message_reply_markup":
                chat_id = k.get("chat_id", a[0] if len(a) > 0 else None)
                mid = k.get("message_id", a[1] if len(a) > 1 else None)
                text = None
            else:
                text = k.get(argname, a[0] if len(a) > 0 else None)
                chat_id = k.get("chat_id", a[1] if len(a) > 1 else None)
                mid = k.get("message_id", a[2] if len(a) > 2 else None)
            route = _wg_route(chat_id)
            if route is None:
                return orig(*a, **k)
            kind, key, st = route
            mk = k.get("reply_markup")
            if kind == "dm":
                with _WG_LOCK:
                    e = st["dm"].get(key, {}).get(mid)
                    old = e["x"] if e else ""
                _wg_dm_put(st, key, mid, text if text is not None else old, mk)
            else:
                with _WG_LOCK:
                    for it in st["feed"]:
                        if it.get("mid") == mid:
                            if text is not None:
                                it["x"] = _wg_clean(text)
                            if name == "edit_message_reply_markup" or "reply_markup" in k:
                                _nb = _wg_buttons(mk)
                                if _nb:
                                    it["b"] = _nb
                                else:
                                    it.pop("b", None)
                _wg_bump(st)
            return _NS(message_id=mid, chat=_NS(id=chat_id), text=text)
        w.__name__ = name
        return w

    for n, an in (("edit_message_text", "text"), ("edit_message_caption", "caption"), ("edit_message_reply_markup", None)):
        w = _edit(n, an)
        if w:
            setattr(bot, n, w)

    if "delete_message" in _WG_ORIG:
        _od = _WG_ORIG["delete_message"]

        def delete_message(chat_id, message_id, *a, **k):
            route = _wg_route(chat_id)
            if route is None:
                return _od(chat_id, message_id, *a, **k)
            kind, key, st = route
            if kind == "dm":
                with _WG_LOCK:
                    st["dm"].get(key, {}).pop(message_id, None)
                _wg_bump(st)
            return True
        bot.delete_message = delete_message

    if "answer_callback_query" in _WG_ORIG:
        _oa = _WG_ORIG["answer_callback_query"]

        def answer_callback_query(callback_query_id, text=None, show_alert=None, *a, **k):
            cid = str(callback_query_id)
            if cid.startswith("wg:"):
                try:
                    uid = int(cid.split(":")[1])
                    chat = WG_UID.get(uid)
                    st = WGS.get(chat) if chat else None
                    if st is not None and text:
                        _wg_toast(st, uid, text, bool(show_alert))
                except Exception:
                    pass
                return True
            return _oa(callback_query_id, text, show_alert, *a, **k)
        bot.answer_callback_query = answer_callback_query

    if "send_chat_action" in _WG_ORIG:
        _oc = _WG_ORIG["send_chat_action"]

        def send_chat_action(chat_id, *a, **k):
            if _wg_route(chat_id) is not None:
                return True
            return _oc(chat_id, *a, **k)
        bot.send_chat_action = send_chat_action

    if "pin_chat_message" in _WG_ORIG:
        _op = _WG_ORIG["pin_chat_message"]

        def pin_chat_message(chat_id, *a, **k):
            if _wg_route(chat_id) is not None:
                return True
            return _op(chat_id, *a, **k)
        bot.pin_chat_message = pin_chat_message

    globals()["_WG_INSTALLED"] = True


def _wg_tg(chat_id, text, markup=None):
    """Guruhga/ishtirokchiga HAQIQIY Telegram xabari (o'rovchisiz)."""
    fn = _WG_ORIG.get("send_message") or bot.send_message
    try:
        return fn(chat_id, text, reply_markup=markup)
    except Exception:
        _logger.debug("wg telegram xabari yuborilmadi", exc_info=True)
        return None


# ------------------------------------------------------------------------------
#  Havolalar
# ------------------------------------------------------------------------------
def wg_start_param(chat_id):
    return "wg" + str(chat_id).replace("-", "m")


def wg_parse_param(p):
    try:
        if p and p.startswith("wg"):
            return int(p[2:].replace("m", "-"))
    except Exception:
        pass
    return None


def _wg_bot_username():
    global BOT_USERNAME
    if not BOT_USERNAME:
        try:
            BOT_USERNAME = bot.get_me().username
        except Exception:
            pass
    return BOT_USERNAME or "HanterMafiaBot"


def wg_group_url(chat_id):
    return f"https://t.me/{_wg_bot_username()}?startapp={wg_start_param(chat_id)}"


def wg_base_url():
    for k in ("API_BASE_URL", "RAILWAY_PUBLIC_DOMAIN", "RENDER_EXTERNAL_URL"):
        v = globals().get(k) or os.environ.get(k)
        if v:
            v = str(v).strip().rstrip("/")
            if not v.startswith("http"):
                v = "https://" + v
            return v
    return "https://hunter-mafia-production.up.railway.app"


def wg_webapp_url(chat_id):
    return f"{wg_base_url()}/wg?c={chat_id}"


# ------------------------------------------------------------------------------
#  Lobbi e'loni (guruhdagi pinlangan xabar)
# ------------------------------------------------------------------------------
def _wg_announce_text(st, game):
    mx = wg_max_players()
    n = len(game["players"])
    lines = ["🎲 <b>Ro'yxatga olish davom etmoqda</b>",
             "📱 <i>Mini App o'yini — Hunter Mafia</i>"]
    if n:
        lines.append("\n<b>Ro'yxatdan o'tgan o'yinchilar:</b>\n")
        try:
            lines.append(player_inline_list(game))
        except Exception:
            lines.append(", ".join(esc(p["name"]) for p in game["players"].values()))
    lines.append(f"\n<b>Jami:</b> {n}/{mx}")
    lines.append("\n⏳ <i>Admin o'yinni boshlashini kutmoqda.</i>")
    return "\n".join(lines)


def _wg_announce_markup(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📱 Mini App'da qo'shilish", url=wg_group_url(chat_id)))
    return kb


def _wg_announce_refresh(chat_id, force=False):
    st = WGS.get(chat_id)
    g = GAMES.get(chat_id)
    if not st or not g or st.get("ann_mid") is None:
        return
    if not force and time.time() - st["ann_ts"] < 4:
        return
    st["ann_ts"] = time.time()
    st["ann_dirty"] = False
    try:
        _WG_ORIG.get("edit_message_text", bot.edit_message_text)(
            _wg_announce_text(st, g), chat_id, st["ann_mid"], reply_markup=_wg_announce_markup(chat_id))
    except Exception:
        pass


def _wg_announce_close(chat_id, text):
    st = WGS.get(chat_id)
    if not st or st.get("ann_mid") is None:
        return
    mid = st["ann_mid"]
    try:
        _WG_ORIG.get("edit_message_text", bot.edit_message_text)(text, chat_id, mid, reply_markup=_wg_open_markup(chat_id))
    except Exception:
        pass
    try:
        bot.unpin_chat_message(chat_id, mid)
    except Exception:
        pass


def _wg_open_markup(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📱 Ochish / kuzatish", url=wg_group_url(chat_id)))
    return kb


# ------------------------------------------------------------------------------
#  O'yin yaratish / lobbi
# ------------------------------------------------------------------------------
def wg_create(chat_id, title, creator_uid):
    """Yangi web o'yin lobbisini ochadi. (ok, xabar)"""
    with _glock(chat_id):
        old = GAMES.get(chat_id)
        if old and old.get("phase") != "waiting":
            return False, "⛔ Bu guruhda o'yin allaqachon ketmoqda."
        if old and old.get("join_msg_id"):
            try:
                _close_join_message(chat_id, old["join_msg_id"])
            except Exception:
                pass
        if old:
            _wg_cleanup(chat_id, notify=False)
        g = new_game(chat_id, title)
        g["web"] = True
        g["squad_mode"] = False
        g["couple_mode"] = False
        g["anon"] = False
        try:
            _gl = bot.export_chat_invite_link(chat_id)
            g["group_link"] = _gl if isinstance(_gl, str) else None
        except Exception:
            pass
        GAMES[chat_id] = g
        st = _wg_new_state(chat_id, title, creator_uid)
        WGS[chat_id] = st
    sent = _wg_tg(chat_id, _wg_announce_text(st, g), _wg_announce_markup(chat_id))
    if sent is not None:
        st["ann_mid"] = sent.message_id
        try:
            bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
        except Exception:
            pass
    th = threading.Thread(target=_wg_lobby_loop, args=(chat_id, st), daemon=True)
    th.start()
    _wg_feed_add(st, "📱 O'yin xonasi ochildi. Qo'shiling!", "sys")
    return True, "ok"


def _wg_cleanup(chat_id, notify=True):
    st = WGS.pop(chat_id, None)
    g = GAMES.get(chat_id)
    if g:
        for t in list(g.get("timers", [])):
            try:
                t.cancel()
            except Exception:
                pass
        GAMES.pop(chat_id, None)
    for u in [u for u, c in list(WG_UID.items()) if c == chat_id]:
        WG_UID.pop(u, None)
    if st:
        st["ended"] = True
        _wg_bump(st)


def wg_join(uid, name, chat_id):
    st = WGS.get(chat_id)
    g = _wg_game(chat_id)
    if not st or not g or st["ended"]:
        return False, "O'yin topilmadi."
    if g.get("phase") != "waiting" or st.get("started"):
        return False, "O'yin allaqachon boshlangan — kuzatuvchi bo'lib kirishingiz mumkin."
    if uid not in g["players"] and len(g["players"]) >= wg_max_players():
        return False, "Xona to'la."
    prev = WG_UID.get(uid)
    status = do_join(chat_id, _NS(id=uid, first_name=name))
    if status == "banned":
        return False, "⛔ Siz bloklangansiz."
    if status in ("no_game", "need_squad", "need_couple", "other_game"):
        return False, "Hozir qo'shilib bo'lmaydi."
    WG_UID[uid] = chat_id
    if prev and prev != chat_id and prev in WGS:
        _wg_bump(WGS[prev])
        WGS[prev]["ann_dirty"] = True
    st["ann_dirty"] = True
    _wg_bump(st)
    return True, "ok"


def _wg_leave_game(uid, chat_id):
    """Lobbida — jimgina chiqadi. O'yin boshlangan bo'lsa — o'yinni tark etadi (o'lik deb belgilanadi)."""
    st = WGS.get(chat_id)
    g = _wg_game(chat_id)
    if not st or not g:
        return False, "O'yin topilmadi."
    p = g["players"].get(uid)
    if not p:
        WG_UID.pop(uid, None)
        return True, "ok"
    if g["phase"] == "waiting":
        with _glock(chat_id):
            g["players"].pop(uid, None)
        WG_UID.pop(uid, None)
        st["ann_dirty"] = True
        _wg_bump(st)
        return True, "ok"
    if p.get("alive"):
        p["alive"] = False
        p["left_game"] = True
        try:
            add_points(uid, LEAVE_POINTS, "leave")
        except Exception:
            pass
        _wg_feed_add(st, f"🚪 <b>{esc(p['name'])}</b> o'yinni tark etdi.", "g")
        try:
            handle_death_side_effects(g, chat_id, uid)
        except Exception:
            _logger.debug("wg leave side effects", exc_info=True)
        try:
            check_and_end_game(chat_id)
        except Exception:
            _logger.debug("wg leave check_end", exc_info=True)
    _wg_bump(st)
    return True, "ok"


def _wg_can_admin(uid, chat_id):
    st = WGS.get(chat_id)
    if not st:
        return False
    if uid == st["creator"] or is_owner(uid):
        return True
    try:
        m = _NS(chat=_NS(id=chat_id, type="supergroup"), from_user=_NS(id=uid), message_id=0, text="")
        return bool(is_authorized(m))
    except Exception:
        return False


def wg_start(uid, chat_id, auto=False):
    st = WGS.get(chat_id)
    g = _wg_game(chat_id)
    if not st or not g or g["phase"] != "waiting" or st.get("started"):
        return False, "O'yin topilmadi."
    if not auto and not _wg_can_admin(uid, chat_id):
        return False, "Faqat guruh admini boshlay oladi."
    mn = game_min_players(g)
    if len(g["players"]) < mn:
        return False, f"Kamida {mn} ta o'yinchi kerak."
    starter = OWNER_ID or uid
    st["starting"] = True
    st["started"] = True
    st["bgm"] = None
    n = len(g["players"])
    try:
        _wg_announce_close(chat_id, f"📱 <b>MINI APP O'YINI boshlandi</b> — {n} ta o'yinchi.")
        _WG_TL.mode = None
        msg = _NS(chat=_NS(id=chat_id, type="supergroup", title=st["title"]), from_user=_NS(id=starter),
                  message_id=0, text="/startgame")
        cmd_startgame(msg)
    except Exception:
        _logger.exception("wg_start xatosi")
        st["starting"] = False
        st["started"] = False
        return False, "Boshlashda xatolik."
    finally:
        st["starting"] = False
    g2 = GAMES.get(chat_id)
    if g2 and g2.get("players") and all(pp.get("role") for pp in g2["players"].values()):
        _wg_tg(chat_id, f"📱 <b>Web o'yin boshlandi!</b> {n} ta o'yinchiga rol berildi.\nO'yin Mini App ichida davom etadi.",
               _wg_open_markup(chat_id))
        _wg_bump(st)
        return True, "ok"
    st["started"] = False
    return False, "O'yin boshlanmadi."


def wg_cancel(uid, chat_id):
    st = WGS.get(chat_id)
    g = _wg_game(chat_id)
    if not st or not g:
        return False, "O'yin topilmadi."
    if not _wg_can_admin(uid, chat_id):
        return False, "Faqat guruh admini bekor qila oladi."
    if g["phase"] == "waiting":
        _wg_announce_close(chat_id, "❌ Web o'yin bekor qilindi.")
    _wg_feed_add(st, "❌ O'yin bekor qilindi.", "sys")
    st["result"] = {"cancelled": True}
    _wg_cleanup(chat_id)
    return True, "ok"


def _wg_lobby_loop(chat_id, st):
    """Lobbi taymeri: avto-boshlash, e'lonni yangilash."""
    while True:
        time.sleep(1.0)
        if WGS.get(chat_id) is not st or st["ended"]:
            return
        g = GAMES.get(chat_id)
        if not g or not g.get("web"):
            return
        if g["phase"] != "waiting" or st.get("started"):
            return
        n = len(g["players"])
        now = time.time()
        if st["ann_dirty"] or now - st["ann_ts"] >= 15:
            _wg_announce_refresh(chat_id)
        # ❗ Avto-boshlash yo'q: o'yinni faqat admin "Hozir boshlash" bilan boshlaydi.
        if now >= st["lobby_end"]:
            _wg_announce_close(chat_id, "⌛ Admin o'yinni boshlamadi — web o'yin yopildi.")
            _wg_feed_add(st, "⌛ Lobbi vaqti tugadi (admin boshlamadi).", "sys")
            st["result"] = {"cancelled": True}
            _wg_cleanup(chat_id)
            return


# ------------------------------------------------------------------------------
#  Harakatlar: tugma (callback) ko'prigi, chat, so'nggi so'z
# ------------------------------------------------------------------------------
def _wg_make_call(uid, name, chat_id, mid, data):
    payload = {
        "id": f"wg:{uid}:{next(_WG_MID)}",
        "from": {"id": uid, "is_bot": False, "first_name": name or "O'yinchi"},
        "chat_instance": "wg",
        "message": {"message_id": mid, "date": int(time.time()), "chat": {"id": uid, "type": "private", "first_name": name or "O'yinchi"},
                    "text": "wg"},
        "data": data,
    }
    return types.CallbackQuery.de_json(json.dumps(payload))


def _wg_process_call(call):
    bot.process_new_callback_query([call])


def wg_act(uid, name, chat_id, mid, data):
    st = WGS.get(chat_id)
    if not st or st["ended"] or WG_UID.get(uid) != chat_id:
        return False, "O'yinda emassiz."
    with _WG_LOCK:
        e = st["dm"].get(uid, {}).get(mid)
        allowed = bool(e) and any(b["d"] == data for row in e.get("b", []) for b in row)
        if not allowed:
            for it in st["feed"]:
                if it.get("mid") == mid and any(b["d"] == data for row in it.get("b", []) for b in row):
                    allowed = True
                    break
    if not allowed:
        return False, "Bu tugma eskirgan."
    if not _rate_ok(uid, "wg_act", 30, 20):
        return False, "Juda tez."
    try:
        call = _wg_make_call(uid, name, chat_id, mid, data)
        _wg_process_call(call)
    except Exception:
        _logger.exception("wg_act xatosi")
        return False, "Xatolik."
    return True, "ok"


def _wg_say_ok(st, uid):
    now = time.time()
    last = _WG_RATE.get(uid, 0)
    if now - last < 1.0:
        return False
    _WG_RATE[uid] = now
    return True


def wg_say(uid, name, chat_id, text, chan):
    st = WGS.get(chat_id)
    g = GAMES.get(chat_id)
    if not st or st["ended"]:
        if st and st["ended"] and chan == "all":
            pass
        else:
            return False, "O'yin topilmadi."
    text = re.sub(r"\s+", " ", (text or "")).strip()[:300]
    if not text:
        return False, "Bo'sh xabar."
    if not _wg_say_ok(st, uid):
        return False, "Sekinroq."
    phase = g.get("phase") if g else "ended"
    p = g["players"].get(uid) if g else None
    alive = bool(p and p.get("alive"))
    muted = False
    try:
        muted = bool(g and (uid in (g.get("afsungar_muted") or set()) or uid in (g.get("day_silenced_chat") or set())))
    except Exception:
        muted = False
    item = {"u": uid, "n": name, "x": text, "t": int(time.time())}
    if chan == "all":
        if phase == "waiting" or st["ended"] or (phase == "day" and alive and not muted):
            pass
        elif phase == "day" and muted:
            return False, "🔇 Siz bugun yoza olmaysiz."
        else:
            return False, "Hozir umumiy chat yopiq."
        with _WG_LOCK:
            st["cid"] += 1
            item["i"] = st["cid"]
            st["chat"].append(item)
            del st["chat"][:-WG_CHAT_MAX]
    elif chan == "team":
        if not (p and alive and p.get("role") in MAFIA_ROLES and phase == "night"):
            return False, "Jamoa chati hozir yopiq."
        with _WG_LOCK:
            st["tid"] += 1
            item["i"] = st["tid"]
            st["team"].append(item)
            del st["team"][:-WG_CHAT_MAX]
    elif chan == "dead":
        if not (p and not alive):
            return False, "Faqat o'liklar yoza oladi."
        with _WG_LOCK:
            st["did"] += 1
            item["i"] = st["did"]
            st["dead"].append(item)
            del st["dead"][:-WG_CHAT_MAX]
    else:
        return False, "Noma'lum chat."
    _wg_bump(st)
    return True, "ok"


def wg_last_word(uid, name, chat_id, text):
    g = _wg_game(chat_id)
    st = WGS.get(chat_id)
    if not g or not st:
        return False, "O'yin topilmadi."
    if uid not in g.get("last_words_wait", set()):
        return False, "Hozir so'nggi so'z yozolmaysiz."
    text = re.sub(r"\s+", " ", (text or "")).strip()[:300]
    if not text:
        return False, "Bo'sh."
    g["last_words_wait"].discard(uid)
    bot.send_message(chat_id, f"🗣 <b>{esc(name)}</b>ning so'nggi so'zi:\n«{esc(text)}»")
    return True, "ok"


# ------------------------------------------------------------------------------
#  🎙 OVOZLI BOSHLOVCHI — slotlar va saqlash
# ------------------------------------------------------------------------------
WGV_MAIN_ROLES = [("don", "Don"), ("mafia", "Mafia"), ("komissar", "Komissar"), ("doktor", "Doktor"),
                  ("serjant", "Serjant"), ("advokat", "Advokat"), ("qotil", "Qotil"), ("daydi", "Daydi"),
                  ("jurnalist", "Jurnalist"), ("mashuqa", "Mashuqa")]

WGV_GROUPS = [
    ("🎮 Lobbi va boshlanish", [("lobby", "Lobbi: xush kelibsiz"), ("game_start", "O'yin boshlandi, rollar tarqatildi")]),
    ("🌙 Tun", [("night_begin", "Shahar uxlaydi (tun boshlanishi)"), ("wake_generic", "Tungi rol uyg'onadi (umumiy)")]
     + [("wake_" + k, f"{v} uyg'onadi") for k, v in WGV_MAIN_ROLES]),
    ("☀️ Tong va kun", [("day_begin", "Shahar uyg'onadi (tong)"), ("death_none", "Bu tunda hech kim o'lmadi"),
                        ("death_some", "Bu tunda kimdir halok bo'ldi"), ("discuss", "Muhokama boshlandi"),
                        ("vote_begin", "Ovoz berish boshlandi"), ("lynch", "Kimdir osildi"), ("lynch_none", "Hech kim osilmadi")]),
    ("🏁 Yakun", [("win_town", "Shahar g'alabasi"), ("win_mafia", "Mafiya g'alabasi"), ("win_solo", "Yakka rol g'alabasi")]),
    ("🎵 Fon musiqa (takrorlanadi)", [("bgm_lobby", "Lobbi musiqasi"), ("bgm_night", "Tun musiqasi"),
                                      ("bgm_day", "Kun musiqasi"), ("bgm_vote", "Ovoz berish musiqasi")]),
]
WGV_ALL = {k: lbl for _g, items in WGV_GROUPS for k, lbl in items}
_WGV_WAIT = {}    # owner uid -> slot (fayl kutilmoqda)
_WGV_CACHE_DIR = os.path.join(os.environ.get("DB_DIR") or os.path.dirname(os.path.abspath(__file__)), "wgv_cache")


def wgv_list(slot):
    try:
        v = json.loads(get_setting("wgv_" + slot) or "[]")
        return v if isinstance(v, list) else []
    except Exception:
        return []


def wgv_set(slot, items):
    set_setting("wgv_" + slot, json.dumps(items))


def wgv_add(slot, fid, dur, mime, name=""):
    items = wgv_list(slot)
    items.append({"fid": fid, "dur": int(dur or 0), "mime": mime or "audio/mpeg", "name": (name or "")[:60]})
    wgv_set(slot, items[-12:])
    return len(items[-12:])


def _wgv_url(slot, idx, entry):
    return f"/wgv/{slot}/{idx}?f={_wg_hashlib.md5(entry['fid'].encode()).hexdigest()[:10]}"


def wgv_pick(slot):
    items = wgv_list(slot)
    if not items:
        return None
    idx = random.randrange(len(items))
    e = items[idx]
    dur = int(e.get("dur") or 0)
    return {"url": _wgv_url(slot, idx, e), "dur": dur if dur > 0 else 4, "slot": slot}


def wg_voice_queue(st, slots):
    """Slotlarni ketma-ket navbatga qo'yadi. Qaytaradi: hammasi tugaguncha necha soniya kutish kerak."""
    now = time.time()
    with _WG_LOCK:
        t = max(now, st.get("voice_busy", 0))
        for slot in slots:
            v = wgv_pick(slot)
            if not v:
                continue
            st["vid"] += 1
            st["voice"].append({"id": st["vid"], "slot": slot, "url": v["url"], "dur": v["dur"], "at": t})
            t += v["dur"] + 0.4
        st["voice"] = st["voice"][-12:]
        st["voice_busy"] = t
    if slots:
        _wg_bump(st)
    return max(0.0, t - now)


def wg_voice_then(st, slots, fn):
    """Ovoz tugagach fn() ni bajaradi (hech qanday ovoz bo'lmasa — darhol)."""
    delay = wg_voice_queue(st, slots)
    if delay <= 0.2:
        fn()
        return
    t = threading.Timer(delay, fn)
    t.daemon = True
    t.start()


def _wgv_fetch(slot, idx):
    """Telegramdan faylni oladi (diskda keshlaydi). (path, mime) yoki None."""
    items = wgv_list(slot)
    if not (0 <= idx < len(items)):
        return None
    e = items[idx]
    os.makedirs(_WGV_CACHE_DIR, exist_ok=True)
    key = _wg_hashlib.md5(e["fid"].encode()).hexdigest()
    path = os.path.join(_WGV_CACHE_DIR, key)
    if not os.path.isfile(path) or os.path.getsize(path) < 100:
        fi = bot.get_file(e["fid"])
        data = bot.download_file(fi.file_path)
        with open(path + ".tmp", "wb") as f:
            f.write(data)
        os.replace(path + ".tmp", path)
    return path, e.get("mime") or "audio/mpeg"


# ------------------------------------------------------------------------------
#  🎭 Personajlar (GLB) va 🏛 xona rasmi — owner bot ichida yuklaydi, Telegram'da saqlanadi
# ------------------------------------------------------------------------------
WGA_KINDS = {"m": "🧑 Erkak personajlar (GLB)", "f": "👩 Ayol personajlar (GLB)", "room": "🏛 Xona rasmi"}
_WGA_WAIT = {}    # owner uid -> kind
WGA_MAX_GLB = 18 * 1024 * 1024


def wga_list(kind):
    try:
        v = json.loads(get_setting("wga_" + kind) or "[]")
        return v if isinstance(v, list) else []
    except Exception:
        return []


def wga_set(kind, items):
    set_setting("wga_" + kind, json.dumps(items))


def _wga_url(kind, idx, e):
    return f"/wga/{kind}/{idx}?f={_wg_hashlib.md5(e['fid'].encode()).hexdigest()[:10]}"


def _wga_fetch(kind, idx):
    items = wga_list(kind)
    if kind not in WGA_KINDS or not (0 <= idx < len(items)):
        return None
    e = items[idx]
    os.makedirs(_WGV_CACHE_DIR, exist_ok=True)
    path = os.path.join(_WGV_CACHE_DIR, _wg_hashlib.md5(e["fid"].encode()).hexdigest())
    if not os.path.isfile(path) or os.path.getsize(path) < 100:
        fi = bot.get_file(e["fid"])
        data = bot.download_file(fi.file_path)
        with open(path + ".tmp", "wb") as f:
            f.write(data)
        os.replace(path + ".tmp", path)
    return path, e.get("mime") or "application/octet-stream"


def wga_public():
    """Klient uchun: yuklangan modellar va xona rasmi."""
    models = []
    for kind in ("m", "f"):
        for i, e in enumerate(wga_list(kind)):
            models.append({"n": e.get("name") or f"{kind}{i}", "g": kind, "u": _wga_url(kind, i, e), "v": int(e.get("size") or 0)})
    room = wga_list("room")
    return models, (_wga_url("room", len(room) - 1, room[-1]) if room else None)


def _wg_send_file(h, path, mime):
    size = os.path.getsize(path)
    rng = h.headers.get("Range")
    start, end = 0, size - 1
    status = 200
    if rng and rng.startswith("bytes="):
        try:
            a, b = rng[6:].split("-", 1)
            start = int(a) if a else max(0, size - int(b))
            end = int(b) if (a and b) else size - 1
            end = min(end, size - 1)
            if start > end or start >= size:
                h.send_response(416)
                h.send_header("Content-Range", f"bytes */{size}")
                h.end_headers()
                return
            status = 206
        except Exception:
            start, end, status = 0, size - 1, 200
    h.send_response(status)
    h.send_header("Content-Type", mime)
    h.send_header("Accept-Ranges", "bytes")
    h.send_header("Cache-Control", "public, max-age=86400")
    h.send_header("Access-Control-Allow-Origin", "*")
    if status == 206:
        h.send_header("Content-Range", f"bytes {start}-{end}/{size}")
    h.send_header("Content-Length", str(end - start + 1))
    h.end_headers()
    with open(path, "rb") as f:
        f.seek(start)
        left = end - start + 1
        while left > 0:
            chunk = f.read(min(65536, left))
            if not chunk:
                break
            h.wfile.write(chunk)
            left -= len(chunk)


def _wg_role_slug(role):
    first = (role or "").split(" ")[0].lower()
    first = re.sub(r"[^a-z]", "", first)
    for k, _v in WGV_MAIN_ROLES:
        if first == k:
            return "wake_" + k
    return "wake_generic"


def _wg_bgm_for(st, g):
    if st["ended"] or not g:
        return None
    ph = g.get("phase")
    slot = {"waiting": "bgm_lobby", "night": "bgm_night"}.get(ph)
    if ph == "day":
        slot = "bgm_vote" if g.get("day_sub_phase") == "voting" else "bgm_day"
    if not slot:
        return None
    v = wgv_list(slot)
    if not v:
        return None
    return {"slot": slot, "url": _wgv_url(slot, 0, v[0])}


# ------------------------------------------------------------------------------
#  Holat (view) — har bir o'yinchi uchun alohida
# ------------------------------------------------------------------------------
def _wg_snapshot_players(g):
    out = []
    for u, p in g["players"].items():
        out.append({"u": u, "n": p.get("name"), "r": p.get("role"), "a": bool(p.get("alive")), "l": bool(p.get("left_game"))})
    return out


def wg_view(uid, name, chat_id, fs=0, cs=0, ts=0, ds=0, vs=0):
    st = WGS.get(chat_id)
    if not st:
        return {"ok": False, "error": "no_game"}
    g = GAMES.get(chat_id) if not st["ended"] else None
    if g is not None and not g.get("web"):
        g = None
    now = time.time()
    ended = st["ended"] or g is None
    phase = "ended" if ended else g.get("phase")
    if phase == "waiting" and st.get("started"):
        phase = "starting"
    P = g["players"] if g else {}
    me_p = P.get(uid)
    in_game = bool(me_p)
    alive = bool(me_p and me_p.get("alive"))
    role = me_p.get("role") if me_p else None
    snap = st.get("final") or []
    if g is None and snap:
        _ms = next((x for x in snap if x["u"] == uid), None)
        if _ms:
            in_game, alive, role = True, bool(_ms["a"]), _ms["r"]
    mafia_member = bool(role and role in MAFIA_ROLES and alive)
    if not in_game:
        st["spec"][uid] = now
    for k in [k for k, v in st["spec"].items() if now - v > 45]:
        st["spec"].pop(k, None)

    reveal_all = ended or (in_game and not alive and phase not in ("waiting",)) or False
    votes = (g.get("votes") or {}) if g else {}
    counts = {}
    voters = {}
    for vtr, tgt in votes.items():
        if tgt != "skip":
            counts[tgt] = counts.get(tgt, 0) + 1
            voters.setdefault(tgt, []).append(vtr)
    pub_votes = bool(g and gsv(g, "vote_public") != "0")

    players = []
    if g:
        seat = 0
        for u, p in P.items():
            seat += 1
            e = {"u": u, "n": p.get("name"), "a": bool(p.get("alive")), "s": seat, "l": bool(p.get("left_game")), "gd": wg_gender(u)}
            if reveal_all or u == uid or (mafia_member and p.get("role") in MAFIA_ROLES):
                e["r"] = p.get("role")
                e["tm"] = team_of(p.get("role")) if p.get("role") else None
            if phase == "day" and g.get("voting_open"):
                e["v"] = counts.get(u, 0)
                if pub_votes and u in voters:
                    e["vb"] = voters[u][:30]
            players.append(e)
    else:
        seat = 0
        for s_ in snap:
            seat += 1
            players.append({"u": s_["u"], "n": s_["n"], "a": s_["a"], "s": seat, "r": s_["r"], "l": s_["l"], "gd": wg_gender(s_["u"]),
                            "tm": team_of(s_["r"]) if s_["r"] else None, "w": s_.get("w")})

    # shaxsiy so'rovlar va eslatmalar
    prompts, notes = [], []
    pidset = {pl["u"] for pl in players}
    with _WG_LOCK:
        d = list(st["dm"].get(uid, {}).values())
        toasts = st["toast"].pop(uid, [])
    for e in d:
        if e.get("b"):
            rows = []
            for row in e["b"]:
                r2 = []
                for b in row:
                    item = {"t": b["t"], "d": b["d"]}
                    try:
                        last = b["d"].split("|")[-1]
                        if last.lstrip("-").isdigit() and int(last) in pidset:
                            item["pu"] = int(last)
                    except Exception:
                        pass
                    r2.append(item)
                rows.append(r2)
            prompts.append({"mid": e["mid"], "x": e["x"], "b": rows, "n": e["n"]})
        else:
            notes.append({"i": e["n"], "x": e["x"], "t": int(e.get("ts", now))})
    if ended:
        notes += [{"i": pr["n"], "x": pr["x"], "t": int(now)} for pr in prompts]
        prompts = []
    prompts.sort(key=lambda z: z["n"])
    notes.sort(key=lambda z: z["i"])
    notes = notes[-40:]

    feed = [it for it in st["feed"] if it["i"] > fs][-200:]
    chat = [it for it in st["chat"] if it["i"] > cs][-100:]
    team = [it for it in st["team"] if it["i"] > ts][-100:] if (mafia_member or ended) else []
    dead = [it for it in st["dead"] if it["i"] > ds][-100:] if ((in_game and not alive) or ended) else []

    muted = False
    try:
        muted = bool(g and uid in (g.get("afsungar_muted") or set()))
    except Exception:
        pass
    can = {
        "all": bool(ended or phase == "waiting" and in_game or (phase == "day" and alive and not muted)),
        "team": bool(mafia_member and phase == "night"),
        "dead": bool(in_game and not alive and phase not in ("waiting",)),
        "last": bool(g and uid in g.get("last_words_wait", set())),
    }
    deadline = None
    if g:
        if phase == "waiting":
            deadline = st["lobby_end"]
        else:
            deadline = g.get("phase_deadline")
    out = {
        "ok": True, "ver": st["ver"], "now": now, "chat_id": chat_id, "title": st["title"], "phase": phase,
        "sub": g.get("day_sub_phase") if g else None, "day": (g.get("day_number") if g else 0),
        "night": (g.get("night_count") if g else 0), "deadline": deadline,
        "voting": bool(g and g.get("voting_open")),
        "players": players, "spec": len(st["spec"]),
        "me": {"u": uid, "in": in_game, "alive": alive, "role": role, "gd": wg_gender(uid),
               "team": team_of(role) if role else None,
               "rs": (_wg_role_slug(role)[5:] if role and _wg_role_slug(role) != "wake_generic" else ""),
               "info": _wg_plain(ROLES_INFO.get(role, "")) if role else "",
               "goal": _wg_plain(role_goal_line(role)) if role else "",
               "vote": votes.get(uid) if g else None,
               "mates": ([{"u": u, "n": p.get("name"), "r": p.get("role"), "a": bool(p.get("alive"))}
                          for u, p in P.items() if u != uid and p.get("role") in MAFIA_ROLES] if mafia_member else []),
               "admin": _wg_can_admin(uid, chat_id)},
        "can": can,
        "lobby": {"min": game_min_players(g) if g else 0, "max": wg_max_players(), "end": st["lobby_end"], "auto": False},
        "prompts": prompts, "notes": notes, "feed": feed, "fl": st["fid"],
        "live": [it for it in st["feed"] if it.get("b")][-3:],
        "chat": chat, "cl": st["cid"], "team": team, "tl": st["tid"], "dead": dead, "dl": st["did"],
        "toast": toasts,
        "voice": [v for v in st["voice"] if v["id"] > vs], "vl": st["vid"],
        "bgm": _wg_bgm_for(st, g),
        "result": st.get("result"),
        "ev": st.get("ev", [])[-8:], "eid": st.get("eid", 0),
        "mode": {"link": wg_group_url(chat_id)},
    }
    return out


def wg_lobbies(uid):
    """Foydalanuvchi uchun: ochiq lobbilar va u ishtirok etayotgan o'yin."""
    items = []
    for cid, st in list(WGS.items()):
        g = GAMES.get(cid)
        if st["ended"] or not g or not g.get("web"):
            continue
        items.append({"c": cid, "t": st["title"], "ph": g.get("phase"), "n": len(g["players"]),
                      "max": wg_max_players(), "mine": WG_UID.get(uid) == cid})
    items.sort(key=lambda z: (not z["mine"], z["ph"] != "waiting"))
    return {"ok": True, "items": items[:30], "mine": WG_UID.get(uid)}


# ------------------------------------------------------------------------------
#  Dvigatel funksiyalariga ulanish (hook): ovoz, qisqa xabarlar, yakun
# ------------------------------------------------------------------------------
def _wg_ev(st, kind, uids):
    """🎬 Hamma ko'radigan voqea (tong o'limi, osilish) — mini-app 3D effektlari uchun."""
    try:
        st["eid"] = st.get("eid", 0) + 1
        st.setdefault("ev", []).append({"i": st["eid"], "k": kind, "d": [int(u) for u in uids]})
        del st["ev"][:-12]
    except Exception:
        pass


def _wg_alive_set(g):
    return {u for u, p in g["players"].items() if p.get("alive")}


def _wg_names(g, uids):
    return ", ".join(esc(g["players"][u]["name"]) for u in uids if u in g["players"])


def _wg_install_hooks():
    G = globals()
    if G.get("_wg_hooks_done"):
        return
    o_start_night = G["start_night"]
    o_start_day = G["start_day"]
    o_open_vote = G["open_day_voting"]
    o_resolve_day = G["resolve_day"]
    o_end_game = G["end_game"]
    o_do_join = G["do_join"]
    o_game_times = G["game_times"]

    def game_times(game_or_chat):
        g = game_or_chat if isinstance(game_or_chat, dict) else GAMES.get(game_or_chat)
        if isinstance(g, dict) and g.get("web"):
            return wg_times()
        return o_game_times(game_or_chat)
    G["game_times"] = game_times

    def start_night(chat_id):
        g = _wg_game(chat_id)
        st = WGS.get(chat_id)
        if not g or not st or st["ended"]:
            return o_start_night(chat_id)
        slots = []
        if st.get("day_alive") is not None and g.get("night_count", 0) > 0:
            died = st["day_alive"] - _wg_alive_set(g)
            slots.append("lynch" if died else "lynch_none")
        st["day_alive"] = None
        if g.get("night_count", 0) == 0:
            slots.append("game_start")
        slots.append("night_begin")
        present = {_wg_role_slug(p.get("role")) for p in g["players"].values() if p.get("alive") and p.get("role")}
        for k, _lbl in WGV_MAIN_ROLES:
            if "wake_" + k in present:
                slots.append("wake_" + k)
        if any(_wg_role_slug(p.get("role")) == "wake_generic" for p in g["players"].values() if p.get("alive") and p.get("role")):
            slots.append("wake_generic")

        def go():
            if WGS.get(chat_id) is not st or st["ended"] or GAMES.get(chat_id) is not g:
                return
            st["night_alive"] = _wg_alive_set(g)
            o_start_night(chat_id)
            if g.get("phase") == "night":
                _wg_tg(chat_id, f"🌙 <b>{g.get('night_count', 1)}-tun.</b> Shahar uxlaydi.", _wg_open_markup(chat_id))
            _wg_bump(st)
        wg_voice_then(st, slots, go)

    def start_day(chat_id):
        g = _wg_game(chat_id)
        st = WGS.get(chat_id)
        if not g or not st or st["ended"]:
            return o_start_day(chat_id)
        died = st.get("night_alive", set()) - _wg_alive_set(g)
        slots = ["day_begin", "death_some" if died else "death_none", "discuss"]

        def go():
            if WGS.get(chat_id) is not st or st["ended"] or GAMES.get(chat_id) is not g:
                return
            o_start_day(chat_id)
            st["day_alive"] = _wg_alive_set(g)
            _wg_ev(st, "dawn", died)
            if died:
                _wg_tg(chat_id, f"☀️ <b>{g.get('day_number', 1)}-kun.</b> Tunda halok bo'ldi: {_wg_names(g, died)}.", _wg_open_markup(chat_id))
            else:
                _wg_tg(chat_id, f"☀️ <b>{g.get('day_number', 1)}-kun.</b> Tun tinch o'tdi — hech kim halok bo'lmadi.", _wg_open_markup(chat_id))
            _wg_bump(st)
        wg_voice_then(st, slots, go)

    def open_day_voting(chat_id):
        g = _wg_game(chat_id)
        st = WGS.get(chat_id)
        if not g or not st or st["ended"]:
            return o_open_vote(chat_id)

        def go():
            if WGS.get(chat_id) is not st or st["ended"] or GAMES.get(chat_id) is not g:
                return
            o_open_vote(chat_id)
            _wg_bump(st)
        wg_voice_then(st, ["vote_begin"], go)

    def resolve_day(chat_id):
        g = _wg_game(chat_id)
        st = WGS.get(chat_id)
        if not g or not st or st["ended"]:
            return o_resolve_day(chat_id)
        before = _wg_alive_set(g)
        o_resolve_day(chat_id)
        g2 = GAMES.get(chat_id)
        if g2 is g and not st["ended"]:
            died = before - _wg_alive_set(g)
            _wg_ev(st, "lynch", died)
            if died:
                _wg_tg(chat_id, f"⚖️ Ovoz berish yakuni: <b>{_wg_names(g, died)}</b> osildi.")
            else:
                _wg_tg(chat_id, "⚖️ Ovoz berish yakuni: hech kim osilmadi.")
        _wg_bump(st)

    def end_game(chat_id, winners_team, couple_pair=None):
        g = _wg_game(chat_id)
        st = WGS.get(chat_id)
        if not g or not st or st["ended"] or g.get("_ending"):
            return o_end_game(chat_id, winners_team, couple_pair)
        final = []
        for u, p in g["players"].items():
            w = False
            try:
                w = bool(_role_won(g, u, p, winners_team)) and not p.get("left_game")
            except Exception:
                pass
            final.append({"u": u, "n": p.get("name"), "r": p.get("role"), "a": bool(p.get("alive")),
                          "l": bool(p.get("left_game")), "w": w})
        _WG_TL.mode = "both"
        try:
            o_end_game(chat_id, winners_team, couple_pair)
        finally:
            _WG_TL.mode = None
        st["final"] = final
        st["result"] = {"win": str(winners_team), "ts": int(time.time()), "dur": int(time.time() - g.get("started_ts", time.time()))}
        slot = "win_mafia" if winners_team == "mafia" else ("win_town" if winners_team == "town" else "win_solo")
        wg_voice_queue(st, [slot])
        st["ended"] = True
        st["ended_ts"] = time.time()
        for u in list(g["players"]):
            if WG_UID.get(u) == chat_id:
                WG_UID.pop(u, None)
        _wg_bump(st)

    def do_join(chat_id, tg_user, squad=None, via_couple=False):
        g = GAMES.get(chat_id)
        if g and g.get("web") and not getattr(_WG_TL, "joining", False):
            return "no_game"   # web o'yinga faqat Mini App orqali qo'shiladi
        return o_do_join(chat_id, tg_user, squad=squad, via_couple=via_couple)

    G["start_night"] = start_night
    G["start_day"] = start_day
    G["open_day_voting"] = open_day_voting
    G["resolve_day"] = resolve_day
    G["end_game"] = end_game
    G["do_join"] = do_join
    o_gsv = G["gsv"]

    def gsv(game_or_chat, key):
        # Web o'yinda 👍/👎 tasdiqlash yo'q: eng ko'p ovoz olgan darhol osiladi
        if key == "confirm_vote":
            try:
                g = game_or_chat if isinstance(game_or_chat, dict) else GAMES.get(game_or_chat)
                if g and g.get("web"):
                    return "0"
            except Exception:
                pass
        return o_gsv(game_or_chat, key)

    G["gsv"] = gsv
    G["_wg_hooks_done"] = True


_wg_orig_wg_join = wg_join


def wg_join(uid, name, chat_id):   # do_join hook'i uchun bayroq bilan
    _WG_TL.joining = True
    try:
        return _wg_orig_wg_join(uid, name, chat_id)
    finally:
        _WG_TL.joining = False


def _wg_janitor():
    while True:
        time.sleep(60)
        try:
            now = time.time()
            for cid, st in list(WGS.items()):
                g = GAMES.get(cid)
                if not st["ended"] and (not g or not g.get("web")):
                    st["ended"] = True
                    st["ended_ts"] = now
                    for u in [u for u, c in list(WG_UID.items()) if c == cid]:
                        WG_UID.pop(u, None)
                    _wg_bump(st)
                if st["ended"] and now - (st.get("ended_ts") or now) > WG_KEEP_AFTER_END:
                    WGS.pop(cid, None)
                if st["ended"] and not st.get("ended_ts"):
                    st["ended_ts"] = now
            for u, c in list(WG_UID.items()):
                if c not in WGS:
                    WG_UID.pop(u, None)
        except Exception:
            _logger.debug("wg janitor", exc_info=True)


# ------------------------------------------------------------------------------
#  HTTP yo'nalishlari
# ------------------------------------------------------------------------------
def _wg_int(v, d=0):
    try:
        return int(v)
    except Exception:
        return d

# ------------------------------------------------------------------------------
#  JONLI OVOZ (WebRTC signaling) — kunduzi mikrofon orqali suhbat
#  Serverga ovoz o'tmaydi: faqat offer/answer/ice xabarlari. Ovoz o'yinchilar
#  o'rtasida to'g'ridan-to'g'ri (P2P). Gapirayotgan o'yinchi bosganda ulanish
#  ochiladi, qo'yib yuborganda yopiladi — shuning uchun og'ir mesh bo'lmaydi.
# ------------------------------------------------------------------------------
WG_RTC_KINDS = ("offer", "answer", "ice", "talk", "stop")


def _wg_rtc_state(st):
    r = st.get("rtc")
    if r is None:
        r = {"q": {}, "seq": 0, "tv": 0, "peers": {}, "talk": {}, "cond": threading.Condition()}
        st["rtc"] = r
    return r


def _wg_rtc_can(uid, chat_id):
    """(ruxsat, faza). Ovoz: lobbida qo'shilganlar, kunduzi esa faqat tirik o'yinchilar."""
    st = WGS.get(chat_id)
    g = GAMES.get(chat_id)
    if not st or st.get("ended") or not g or not g.get("web"):
        return False, "ended"
    ph = g.get("phase")
    me = (g.get("players") or {}).get(uid)
    if not me:
        return False, ph
    if ph == "day":
        return bool(me.get("alive")), ph
    if ph == "waiting" and not st.get("started"):
        return True, ph
    return False, ph


def _wg_rtc_ice():
    ice = [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]
    u = os.environ.get("WG_TURN_URL", "").strip()
    if u:
        ice.append({"urls": [x.strip() for x in u.split(",") if x.strip()],
                    "username": os.environ.get("WG_TURN_USER", ""),
                    "credential": os.environ.get("WG_TURN_PASS", "")})
    return ice


def wg_rtc_poll(uid, chat_id, since=0, wait=0, tv=-1):
    st = WGS.get(chat_id)
    if not st:
        return {"ok": False, "error": "no_game"}
    r = _wg_rtc_state(st)
    deadline = time.time() + max(0, min(wait, 20))
    while True:
        now = time.time()
        can, ph = _wg_rtc_can(uid, chat_id)
        with r["cond"]:
            if uid not in r["peers"]:
                r["tv"] += 1
                r["cond"].notify_all()
            r["peers"][uid] = now
            for k in [k for k, v in r["peers"].items() if now - v > 40]:
                r["peers"].pop(k, None)
                r["tv"] += 1
                r["talk"].pop(k, None)
            q = r["q"].setdefault(uid, [])
            q[:] = [m for m in q if m["i"] > since][-200:]
            msgs = list(q)
            if ph not in ("day", "waiting"):
                if r["talk"]:
                    r["tv"] += 1
                r["talk"].clear()
            else:
                for k in [k for k, v in r["talk"].items() if now - v > 25]:
                    r["talk"].pop(k, None)
                    r["tv"] += 1
            if msgs or now >= deadline or r["tv"] != tv:
                return {"ok": True, "msgs": msgs, "peers": [k for k in r["peers"] if k != uid][:40],
                        "talk": list(r["talk"].keys()), "tv": r["tv"], "can": can, "ph": ph, "ice": _wg_rtc_ice(),
                        "seq": r["seq"]}
            r["cond"].wait(timeout=min(1.5, max(0.1, deadline - now)))


def wg_rtc_send(uid, chat_id, to, kind, payload):
    st = WGS.get(chat_id)
    if not st:
        return False, "no_game"
    if kind not in WG_RTC_KINDS:
        return False, "bad_kind"
    r = _wg_rtc_state(st)
    can, ph = _wg_rtc_can(uid, chat_id)
    if kind in ("talk", "offer") and not can:
        return False, "Hozir gapirib bo'lmaydi."
    if kind == "stop":
        with r["cond"]:
            if r["talk"].pop(uid, None) is not None:
                r["tv"] += 1
                r["cond"].notify_all()
        return True, "ok"
    if kind == "talk":
        with r["cond"]:
            if uid not in r["talk"]:
                r["tv"] += 1
                r["cond"].notify_all()
            r["talk"][uid] = time.time()
        return True, "ok"
    if ph not in ("day", "waiting"):
        return False, "Hozir gapirib bo'lmaydi."
    try:
        raw = json.dumps(payload)
    except Exception:
        return False, "bad_payload"
    if len(raw) > 8000:
        return False, "too_big"
    with r["cond"]:
        if to not in r["peers"] or to == uid:
            return False, "no_peer"
        r["seq"] += 1
        r["q"].setdefault(to, []).append({"i": r["seq"], "f": uid, "k": kind, "p": payload})
        r["cond"].notify_all()
    return True, "ok"



def wg_route_get(h, parsed):
    p = parsed.path
    if p in ("/wg", "/wg/"):
        try:
            fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webgame.html")
            with open(fp, "rb") as f:
                body = f.read()
            h.send_response(200)
            h.send_header("Content-Type", "text/html; charset=utf-8")
            h.send_header("Cache-Control", "no-cache")
            h.send_header("Content-Length", str(len(body)))
            h.end_headers()
            h.wfile.write(body)
        except Exception:
            h._send_json({"error": "webgame_file_missing"}, status=404)
        return True
    if p.startswith("/wga/"):
        try:
            _x, _y, kind, idx = p.split("/")[:4]
            r = _wga_fetch(kind, _wg_int(idx, -1))
            if not r:
                raise ValueError
            _wg_send_file(h, r[0], r[1])
        except Exception:
            try:
                h._send_json({"error": "not_found"}, status=404)
            except Exception:
                pass
        return True
    if p == "/api/wg/models" or p.startswith("/wgm/"):
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wg_models")
        try:
            if p == "/api/wg/models":
                out = []
                if os.path.isdir(base):
                    for fn in sorted(os.listdir(base)):
                        if re.match(r"^[A-Za-z0-9_.-]+\.glb$", fn):
                            sz = os.path.getsize(os.path.join(base, fn))
                            out.append({"n": fn, "g": "f" if fn.lower().startswith(("f_", "female", "woman")) else "m", "v": sz})
                _up, _room = wga_public()
                h._send_json({"ok": True, "models": out + _up, "room": _room})
                return True
            fn = p[len("/wgm/"):]
            if not re.match(r"^[A-Za-z0-9_.-]+\.glb$", fn):
                raise ValueError
            fp = os.path.join(base, fn)
            with open(fp, "rb") as f:
                body = f.read()
            h.send_response(200)
            h.send_header("Content-Type", "model/gltf-binary")
            h.send_header("Cache-Control", "public, max-age=604800")
            h.send_header("Content-Length", str(len(body)))
            h.end_headers()
            h.wfile.write(body)
        except Exception:
            try:
                h._send_json({"error": "not_found"}, status=404)
            except Exception:
                pass
        return True
    if p.startswith("/wgv/"):
        try:
            _x, _y, slot, idx = p.split("/")[:4] if p.count("/") >= 3 else (None, None, None, None)
            if slot not in WGV_ALL:
                raise ValueError
            r = _wgv_fetch(slot, _wg_int(idx, -1))
            if not r:
                raise ValueError
            _wg_send_file(h, r[0], r[1])
        except Exception:
            try:
                h._send_json({"error": "not_found"}, status=404)
            except Exception:
                pass
        return True
    if not p.startswith("/api/wg/"):
        return False
    qs = parse_qs(parsed.query)
    uid, name = _v8_auth((qs.get("init_data") or [""])[0])
    if uid is None:
        h._send_json({"error": "invalid_init_data"}, status=401)
        return True
    q = lambda k, d="": (qs.get(k) or [d])[0]
    try:
        if p == "/api/wg/state":
            cid = _wg_int(q("c"), 0)
            h._send_json(wg_view(uid, name, cid, _wg_int(q("fs")), _wg_int(q("cs")), _wg_int(q("ts")),
                                 _wg_int(q("ds")), _wg_int(q("vs"))))
        elif p == "/api/wg/lobbies":
            h._send_json(wg_lobbies(uid))
        elif p == "/api/wg/rtc":
            h._send_json(wg_rtc_poll(uid, _wg_int(q("c"), 0), _wg_int(q("since")), _wg_int(q("w")), _wg_int(q("tv"), -1)))
        elif p == "/api/wg/stream":
            _wg_sse(h, uid, _wg_int(q("c"), 0))
        else:
            h._send_json({"error": "not_found"}, status=404)
    except Exception:
        _logger.exception("wg GET xatosi: %s", p)
        try:
            h._send_json({"error": "server_error"}, status=500)
        except Exception:
            pass
    return True


def _wg_sse(h, uid, chat_id):
    st = WGS.get(chat_id)
    h.send_response(200)
    h.send_header("Content-Type", "text/event-stream")
    h.send_header("Cache-Control", "no-cache")
    h.send_header("X-Accel-Buffering", "no")
    h.send_header("Access-Control-Allow-Origin", "*")
    h.end_headers()
    if not st:
        h.wfile.write(b"event: gone\ndata: 0\n\n")
        return
    last = -1
    t_end = time.time() + 600
    try:
        while time.time() < t_end:
            if st["ver"] != last:
                last = st["ver"]
                h.wfile.write(f"data: {last}\n\n".encode())
                h.wfile.flush()
            else:
                h.wfile.write(b": ping\n\n")
                h.wfile.flush()
            with st["cond"]:
                st["cond"].wait(timeout=12)
    except Exception:
        pass


WG_POST_PATHS = {"/api/wg/join", "/api/wg/leave", "/api/wg/start", "/api/wg/cancel", "/api/wg/act",
                 "/api/wg/say", "/api/wg/last", "/api/wg/rtc", "/api/wg/gender", "/api/wg/gesture"}


def wg_route_post(h, path, body):
    if path not in WG_POST_PATHS:
        return False
    uid, name = _v8_auth(body.get("init_data"))
    if uid is None:
        h._send_json({"ok": False, "error": "invalid_init_data"}, status=401)
        return True
    if path == "/api/wg/rtc":
        if not _rate_ok(uid, "wg_rtc", 900, 30):
            h._send_json({"ok": False, "error": "Juda tez."}, status=429)
            return True
        ok, msg = wg_rtc_send(uid, _wg_int(body.get("c"), 0), _wg_int(body.get("to"), 0),
                              str(body.get("k", "")), body.get("p"))
        h._send_json({"ok": ok, "error": None if ok else msg})
        return True
    if not _rate_ok(uid, "wg_post", 90, 30):
        h._send_json({"ok": False, "error": "Juda tez."}, status=429)
        return True
    cid = _wg_int(body.get("c"), 0)
    try:
        if path == "/api/wg/join":
            ok, msg = wg_join(uid, name, cid)
        elif path == "/api/wg/leave":
            ok, msg = _wg_leave_game(uid, cid)
        elif path == "/api/wg/start":
            ok, msg = wg_start(uid, cid)
        elif path == "/api/wg/cancel":
            ok, msg = wg_cancel(uid, cid)
        elif path == "/api/wg/act":
            ok, msg = wg_act(uid, name, cid, _wg_int(body.get("mid")), str(body.get("d", "")))
        elif path == "/api/wg/gender":
            _g0 = _wg_game(cid)
            if _g0 and uid in _g0["players"] and _g0.get("phase") != "waiting":
                ok, msg = False, "O'yin boshlangan — jinsni o'zgartirib bo'lmaydi."
            else:
                wg_gender_set(uid, str(body.get("gd", "m")))
                if cid in WGS:
                    _wg_bump(WGS[cid])
                ok, msg = True, "ok"
        elif path == "/api/wg/gesture":
            _g1, _st1 = _wg_game(cid), WGS.get(cid)
            ok, msg = True, "ok"
            if (_g1 and _st1 and not _st1["ended"] and str(body.get("k")) == "card" and _g1.get("phase") in ("day", "night")
                    and (_g1["players"].get(uid) or {}).get("alive") and _rate_ok(uid, "wg_gest", 1, 8)):
                _wg_ev(_st1, "card", [uid])
                _wg_bump(_st1)
        elif path == "/api/wg/say":
            ok, msg = wg_say(uid, name, cid, str(body.get("x", "")), str(body.get("ch", "all")))
        else:
            ok, msg = wg_last_word(uid, name, cid, str(body.get("x", "")))
        h._send_json({"ok": ok, "error": None if ok else msg})
    except Exception:
        _logger.exception("wg POST xatosi: %s", path)
        h._send_json({"ok": False, "error": "server_error"}, status=500)
    return True


# ------------------------------------------------------------------------------
#  Telegram buyruqlari: /webgame
# ------------------------------------------------------------------------------
def _wg_webapp_button(text, url):
    return types.InlineKeyboardButton(text, web_app=types.WebAppInfo(url=url))


def _wg_resend_running(chat_id, st, g):
    """O'yin ketayotgan bo'lsa — guruhga 'o'yinni ochish' kartasini qayta yuboradi (eskisini o'chiradi)."""
    old = st.get("run_mid")
    if old:
        try:
            _WG_ORIG.get("delete_message", bot.delete_message)(chat_id, old)
        except Exception:
            pass
    ph = {"night": "🌙 Tun", "day": "☀️ Kun"}.get(g.get("phase"), "🎮 O'yin")
    alive = len([1 for p in g["players"].values() if p.get("alive")])
    sent = _wg_tg(chat_id, f"📱 <b>Web o'yin davom etmoqda</b>\n{ph} · tirik: <b>{alive}</b>\nQo'shilish/kuzatish uchun pastdagi tugmani bosing.",
                  _wg_open_markup(chat_id))
    if sent is not None:
        st["run_mid"] = sent.message_id


def wg_resend_for_game_cmd(message):
    """/game: shu guruhda web o'yin (lobbi yoki ketayotgan) bor bo'lsa — yangi klassik lobbi ochmaydi, web kartani qayta yuboradi."""
    chat_id = message.chat.id
    st = WGS.get(chat_id)
    g = GAMES.get(chat_id)
    if not (st and g and g.get("web")) or st["ended"]:
        return False
    safe_delete(message)
    if g.get("phase") == "waiting":
        if st.get("ann_mid"):
            try:
                bot.unpin_chat_message(chat_id, st["ann_mid"])
                bot.delete_message(chat_id, st["ann_mid"])
            except Exception:
                pass
        sent = _wg_tg(chat_id, _wg_announce_text(st, g), _wg_announce_markup(chat_id))
        if sent is not None:
            st["ann_mid"] = sent.message_id
    else:
        _wg_resend_running(chat_id, st, g)
    return True


@bot.message_handler(commands=["webgame", "wg", "webgame_new"])
def cmd_webgame(message):
    maybe_capture_owner(message.from_user)
    uid = message.from_user.id
    if message.chat.type == "private":
        cid = WG_UID.get(uid)
        kb = types.InlineKeyboardMarkup()
        if cid and cid in WGS and not WGS[cid]["ended"]:
            kb.add(_wg_webapp_button("📱 O'yinni ochish", wg_webapp_url(cid)))
            bot.send_message(uid, "📱 <b>Web o'yin</b> davom etmoqda.", reply_markup=kb)
        else:
            kb.add(_wg_webapp_button("📱 Ochiq o'yinlar", wg_base_url() + "/wg"))
            bot.send_message(uid, "📱 <b>Web o'yin</b>\nGuruhda <code>/webgame</code> yozing — o'yin xonasi ochiladi.\n"
                                  "Ochiq xonalarni pastdagi tugmadan ko'ring.", reply_markup=kb)
        return
    if message.chat.type not in ("group", "supergroup"):
        return
    safe_delete(message)
    if not is_authorized(message):
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
        return
    chat_id = message.chat.id
    if bot_admin_state(chat_id) is False:
        bot.send_message(chat_id, "⚠️ Avval meni guruhda <b>admin</b> qiling (xabarlarni o'chirish va qadash huquqi bilan).")
        return
    try:
        add_known_group(chat_id, message.chat.title or "Nomsiz guruh")
    except Exception:
        pass
    st = WGS.get(chat_id)
    g = GAMES.get(chat_id)
    if st and g and g.get("web") and g.get("phase") != "waiting" and not st["ended"]:
        _wg_resend_running(chat_id, st, g)
        return
    if st and g and g.get("web") and g.get("phase") == "waiting" and not st["ended"]:
        # ochiq lobbi bor — e'lonni qayta yuboramiz
        if st.get("ann_mid"):
            try:
                bot.unpin_chat_message(chat_id, st["ann_mid"])
                bot.delete_message(chat_id, st["ann_mid"])
            except Exception:
                pass
        sent = _wg_tg(chat_id, _wg_announce_text(st, g), _wg_announce_markup(chat_id))
        if sent is not None:
            st["ann_mid"] = sent.message_id
            try:
                bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
            except Exception:
                pass
        return
    ok, msg = wg_create(chat_id, message.chat.title, uid)
    if not ok:
        bot.send_message(chat_id, msg)


# ------------------------------------------------------------------------------
#  🎙 Ovozli boshlovchi paneli (owner, bot ichida — tugmalar bilan)
# ------------------------------------------------------------------------------
def _wgv_menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(f"🎭 Personajlar (🧑 {len(wga_list('m'))} · 👩 {len(wga_list('f'))})", callback_data="wgv|a|menu"))
    kb.add(types.InlineKeyboardButton(f"🏛 Xona rasmi ({'✅' if wga_list('room') else 'standart'})", callback_data="wgv|a|room"))
    for gi, (title, items) in enumerate(WGV_GROUPS):
        have = sum(1 for k, _l in items if wgv_list(k))
        kb.add(types.InlineKeyboardButton(f"{title}  ({have}/{len(items)})", callback_data=f"wgv|g|{gi}"))
    kb.add(types.InlineKeyboardButton("⚙️ Sozlamalar", callback_data="wgv|cfg"))
    kb.add(types.InlineKeyboardButton("🔙 Admin panel", callback_data="admin|panel"))
    return kb


def _wgv_menu_text():
    total = len(WGV_ALL)
    have = sum(1 for k in WGV_ALL if wgv_list(k))
    return (f"🎮 <b>Web game sozlamalari</b>\n\n"
            "🎭 <b>Personajlar</b> — erkak/ayol GLB modellar (lobbida Yigit/Qiz tanloviga qarab beriladi)\n"
            "🏛 <b>Xona rasmi</b> — xona fonini rasm bilan almashtirish\n"
            f"🎙 <b>Ovozlar</b> — yozilgan: <b>{have}/{total}</b> ta joy (mp3/m4a, bir joyga bir nechta variant — tasodifiy tanlanadi)\n"
            "⚙️ <b>Sozlamalar</b> — o'yinchilar soni, lobbi va faza vaqtlari\n\n"
            "<i>Bo'limni tanlang.</i>")


@bot.message_handler(commands=["ovoz", "wgovoz"], func=lambda m: m.chat.type == "private")
def cmd_wgv(message):
    if not is_owner(message.from_user.id):
        return
    _WGV_WAIT.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, _wgv_menu_text(), reply_markup=_wgv_menu_kb())


@bot.callback_query_handler(func=lambda c: c.data.startswith("wgv|"))
def cb_wgv(call):
    if not _owner_only(call):
        return
    uid = call.from_user.id
    parts = call.data.split("|")
    act = parts[1]
    if act == "a":
        _WGV_WAIT.pop(uid, None)
        what = parts[2]
        bot.answer_callback_query(call.id)
        if what == "menu":
            _WGA_WAIT.pop(uid, None)
            kb = types.InlineKeyboardMarkup(row_width=1)
            kb.add(types.InlineKeyboardButton(f"🧑 Erkak personajlar ({len(wga_list('m'))})", callback_data="wgv|a|m"),
                   types.InlineKeyboardButton(f"👩 Ayol personajlar ({len(wga_list('f'))})", callback_data="wgv|a|f"),
                   types.InlineKeyboardButton("🔙 Ortga", callback_data="wgv|menu"))
            smart_render(call, "🎭 <b>Personajlar</b>\n\nYigit tanlagan o'yinchiga erkak, Qiz tanlaganga ayol model beriladi. "
                               "Har jinsga bir nechta model yuklasangiz, o'yinchilarga tasodifiy tarqatiladi.\n"
                               "Model yuklanmagan jins uchun oddiy zaxira figura ishlatiladi.", kb)
            return
        if what not in WGA_KINDS:
            return
        _WGA_WAIT[uid] = what
        items = wga_list(what)
        kb = types.InlineKeyboardMarkup(row_width=2)
        for i, e in enumerate(items):
            kb.add(types.InlineKeyboardButton(f"📄 {i + 1}. {(e.get('name') or '')[:22]} ({round(int(e.get('size') or 0) / 1048576, 1)} MB)", callback_data="wgv|a|menu_noop"),
                   types.InlineKeyboardButton(f"🗑 {i + 1}", callback_data=f"wgv|adel|{what}|{i}"))
        kb.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="wgv|a|menu" if what != "room" else "wgv|menu"))
        if what == "room":
            hint = ("📎 Xona rasmini yuboring (JPG/PNG, keng panorama yoki xona fotosi; fayl sifatida yuborsangiz sifati yaxshi). "
                    "Yangisi eskisini almashtiradi. O'chirsangiz standart xona qaytadi.")
        else:
            hint = ("📎 GLB faylni <b>fayl (document)</b> sifatida yuboring (18 MB gacha, mobil uchun 2–5 MB tavsiya).\n"
                    "Talab: skeletli (rigged), 'Idle' animatsiyali, Draco siqishsiz, yuzi +Z tomonga qaragan.")
        smart_render(call, f"{WGA_KINDS[what]}\nYuklangan: <b>{len(items)}</b> ta\n\n{hint}", kb)
        return
    if act == "adel":
        what, idx = parts[2], int(parts[3])
        items = wga_list(what)
        if what in WGA_KINDS and 0 <= idx < len(items):
            items.pop(idx)
            wga_set(what, items)
        bot.answer_callback_query(call.id, "🗑 O'chirildi")
        call.data = f"wgv|a|{what}"
        cb_wgv(call)
        return
    if act == "menu":
        _WGV_WAIT.pop(uid, None)
        _WGA_WAIT.pop(uid, None)
        bot.answer_callback_query(call.id)
        smart_render(call, _wgv_menu_text(), _wgv_menu_kb())
        return
    if act == "g":
        gi = int(parts[2])
        title, items = WGV_GROUPS[gi]
        kb = types.InlineKeyboardMarkup(row_width=1)
        for k, lbl in items:
            n = len(wgv_list(k))
            kb.add(types.InlineKeyboardButton(f"{'✅' if n else '⬜'} {lbl}" + (f" ({n})" if n else ""), callback_data=f"wgv|s|{k}"))
        kb.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="wgv|menu"))
        bot.answer_callback_query(call.id)
        smart_render(call, f"{title}\n\nJoyni tanlang:", kb)
        return
    if act == "s":
        slot = parts[2]
        if slot not in WGV_ALL:
            bot.answer_callback_query(call.id, "Noma'lum.")
            return
        _WGV_WAIT[uid] = slot
        items = wgv_list(slot)
        gi = next(i for i, (_t, its) in enumerate(WGV_GROUPS) if any(k == slot for k, _l in its))
        kb = types.InlineKeyboardMarkup(row_width=2)
        for i, e in enumerate(items):
            kb.add(types.InlineKeyboardButton(f"🔊 {i + 1} ({e.get('dur', 0)}s)", callback_data=f"wgv|play|{slot}|{i}"),
                   types.InlineKeyboardButton(f"🗑 {i + 1}", callback_data=f"wgv|del1|{slot}|{i}"))
        kb.add(types.InlineKeyboardButton("✅ Tayyor", callback_data=f"wgv|g|{gi}"))
        bot.answer_callback_query(call.id)
        smart_render(call, f"🎙 <b>{WGV_ALL[slot]}</b>\nYuklangan variantlar: <b>{len(items)}</b>\n\n"
                           "📎 Endi mp3/m4a audio faylni shu chatga yuboring (15 MB gacha).\n"
                           "Yana yuborsangiz — yangi variant qo'shiladi.", kb)
        return
    if act == "play":
        slot, idx = parts[2], int(parts[3])
        items = wgv_list(slot)
        if 0 <= idx < len(items):
            bot.answer_callback_query(call.id)
            try:
                bot.send_audio(call.message.chat.id, items[idx]["fid"], caption=f"🔊 {WGV_ALL.get(slot, slot)} — {idx + 1}")
            except Exception:
                bot.send_message(call.message.chat.id, "❌ Faylni yuborib bo'lmadi.")
        return
    if act == "del1":
        slot, idx = parts[2], int(parts[3])
        items = wgv_list(slot)
        if 0 <= idx < len(items):
            items.pop(idx)
            wgv_set(slot, items)
        bot.answer_callback_query(call.id, "🗑 O'chirildi")
        call.data = f"wgv|s|{slot}"
        cb_wgv(call)
        return
    if act == "cfg":
        mx = wg_max_players()
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.add(types.InlineKeyboardButton("➖5", callback_data="wgv|set|max|-5"),
               types.InlineKeyboardButton(f"👥 Maks: {mx}", callback_data="wgv|cfg"),
               types.InlineKeyboardButton("➕5", callback_data="wgv|set|max|5"))
        t = wg_times()
        for key, lbl, ico in (("night", "Tun", "🌙"), ("discuss", "Muhokama", "💬"), ("vote", "Ovoz", "🗳")):
            kb.add(types.InlineKeyboardButton("➖10s", callback_data=f"wgv|set|t{key}|-10"),
                   types.InlineKeyboardButton(f"{ico} {lbl}: {t[key]}s", callback_data="wgv|cfg"),
                   types.InlineKeyboardButton("➕10s", callback_data=f"wgv|set|t{key}|10"))
        kb.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="wgv|menu"))
        bot.answer_callback_query(call.id)
        smart_render(call, "⚙️ <b>Web o'yin sozlamalari</b>\n\nO'yinchilar chegarasi va faza vaqtlari (faqat web o'yin). Lobbi avto-boshlanmaydi — o'yinni admin boshlaydi.", kb)
        return
    if act == "set":
        what, delta = parts[2], int(parts[3])
        if what == "max":
            set_setting("wg_max", str(max(3, min(100, wg_max_players() + delta))))
        elif what in ("tnight", "tdiscuss", "tvote"):
            k = what[1:]
            set_setting("wgt_" + k, str(max(15, min(600, wg_times()[k] + delta))))
        else:
            set_setting("wg_lobby_s", str(max(30, min(900, wg_lobby_seconds() + delta))))
        call.data = "wgv|cfg"
        cb_wgv(call)
        return
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=["audio", "voice", "document"],
                     func=lambda m: m.chat.type == "private" and m.from_user.id in _WGV_WAIT)
def wgv_on_file(message):
    uid = message.from_user.id
    if not is_owner(uid):
        _WGV_WAIT.pop(uid, None)
        return
    slot = _WGV_WAIT.get(uid)
    f = message.audio or message.voice or message.document
    if not f:
        return
    mime = getattr(f, "mime_type", None) or ""
    fname = getattr(f, "file_name", None) or ""
    if message.document and not (mime.startswith("audio/") or fname.lower().endswith((".mp3", ".m4a", ".aac", ".ogg", ".wav", ".opus"))):
        bot.send_message(uid, "❌ Bu audio fayl emas. mp3 yoki m4a yuboring.")
        return
    size = int(getattr(f, "file_size", 0) or 0)
    if size > 15 * 1024 * 1024:
        bot.send_message(uid, "❌ Fayl 15 MB dan katta.")
        return
    dur = int(getattr(f, "duration", 0) or 0)
    if dur <= 0 and size:
        dur = max(2, int(size * 8 / 128000))   # taxminiy (128 kbps)
    if not mime:
        mime = "audio/mpeg" if fname.lower().endswith(".mp3") else ("audio/mp4" if fname.lower().endswith(".m4a") else "audio/mpeg")
    n = wgv_add(slot, f.file_id, dur, mime, fname)
    note = ""
    if message.voice:
        note = "\n⚠️ Ovozli xabar (ogg) iPhone'da o'ynamasligi mumkin — mp3/m4a tavsiya etiladi."
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🔊 Eshitish", callback_data=f"wgv|play|{slot}|{n - 1}"),
           types.InlineKeyboardButton("📂 Variantlar", callback_data=f"wgv|s|{slot}"),
           types.InlineKeyboardButton("🔙 Ro'yxat", callback_data="wgv|menu"))
    bot.send_message(uid, f"✅ Saqlandi: <b>{WGV_ALL.get(slot, slot)}</b> — {n}-variant ({dur}s).{note}\n"
                          "Yana fayl yuborsangiz, yangi variant qo'shiladi.", reply_markup=kb)


@bot.message_handler(content_types=["document", "photo"],
                     func=lambda m: m.chat.type == "private" and m.from_user.id in _WGA_WAIT)
def wga_on_file(message):
    uid = message.from_user.id
    if not is_owner(uid):
        _WGA_WAIT.pop(uid, None)
        return
    kind = _WGA_WAIT.get(uid)
    if kind not in WGA_KINDS:
        return
    if message.photo:
        f = message.photo[-1]
        fname, mime = "photo.jpg", "image/jpeg"
    else:
        f = message.document
        fname = getattr(f, "file_name", None) or ""
        mime = getattr(f, "mime_type", None) or ""
    size = int(getattr(f, "file_size", 0) or 0)
    low = fname.lower()
    if kind == "room":
        if not (message.photo or mime.startswith("image/") or low.endswith((".jpg", ".jpeg", ".png", ".webp"))):
            bot.send_message(uid, "❌ Bu rasm emas. JPG yoki PNG yuboring.")
            return
        if size > 12 * 1024 * 1024:
            bot.send_message(uid, "❌ Rasm 12 MB dan katta.")
            return
        if not mime.startswith("image/"):
            mime = "image/png" if low.endswith(".png") else ("image/webp" if low.endswith(".webp") else "image/jpeg")
        wga_set("room", [{"fid": f.file_id, "name": fname[:60], "size": size, "mime": mime}])
        bot.send_message(uid, "✅ Xona rasmi saqlandi. Yangi o'yinlarda (yoki sahifani qayta ochganda) ko'rinadi.\n"
                              "Standart xonaga qaytish: Xona rasmi → 🗑.")
        return
    if message.photo or not low.endswith((".glb",)):
        bot.send_message(uid, "❌ Bu GLB fayl emas. Modelni <b>.glb</b> formatda, <b>fayl (document)</b> sifatida yuboring.")
        return
    if size > WGA_MAX_GLB:
        bot.send_message(uid, "❌ Fayl 18 MB dan katta (Telegram bot limiti 20 MB). Modelni yengilroq eksport qiling.")
        return
    items = wga_list(kind)
    items.append({"fid": f.file_id, "name": fname[:60], "size": size, "mime": "model/gltf-binary"})
    wga_set(kind, items[-10:])
    warn = "\n⚠️ Fayl 6 MB dan katta — sekin telefonlarda yuklanishi og'ir bo'lishi mumkin." if size > 6 * 1048576 else ""
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("📂 Ro'yxat", callback_data=f"wgv|a|{kind}"),
           types.InlineKeyboardButton("🔙 Web game sozlamalari", callback_data="wgv|menu"))
    bot.send_message(uid, f"✅ Saqlandi: <b>{esc(fname)}</b> — {WGA_KINDS[kind]} ({len(items[-10:])}-model).{warn}\n"
                          "Yana fayl yuborsangiz, yangi model qo'shiladi.", reply_markup=kb)


# ------------------------------------------------------------------------------
#  Ishga tushirish
# ------------------------------------------------------------------------------
def wg_boot():
    _wg_install_interceptors()
    _wg_install_hooks()
    threading.Thread(target=_wg_janitor, daemon=True).start()
    _logger.info("📱 Web o'yin moduli yuklandi (v%s)", WG_VERSION)


wg_boot()
