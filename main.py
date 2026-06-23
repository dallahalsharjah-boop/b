"""
╔══════════════════════════════════════════╗
║   By.Abdullah NassEr ♥  — Widget App    ║
║   Kivy + Python → Android APK           ║
╚══════════════════════════════════════════╝
"""

import kivy
kivy.require('2.3.0')

from kivy.app          import App
from kivy.uix.boxlayout   import BoxLayout
from kivy.uix.floatlayout  import FloatLayout
from kivy.uix.label        import Label
from kivy.uix.widget       import Widget
from kivy.uix.scrollview   import ScrollView
from kivy.graphics import (
    Color, RoundedRectangle, Ellipse,
    Line, Rectangle, InstructionGroup
)
from kivy.clock       import Clock
from kivy.core.window import Window
from kivy.metrics     import dp, sp
from kivy.utils       import get_color_from_hex

import datetime
import math
import arabic_reshaper
from bidi.algorithm import get_display
from hijridate import Gregorian

# ── Window setup ──────────────────────────────────────────────────────────────
Window.clearcolor = (0.035, 0.035, 0.035, 1)


# ── Arabic text helper ────────────────────────────────────────────────────────
def ar(text: str) -> str:
    """Reshape and apply BiDi algorithm for correct Arabic rendering in Kivy."""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


# ── Data ──────────────────────────────────────────────────────────────────────
AR_DAYS = [
    'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء',
    'الخميس', 'الجمعة', 'السبت'
]
AR_MONTHS = [
    'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
    'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'
]
HJ_MONTHS = [
    'محرم', 'صفر', 'ربيع الأول', 'ربيع الآخر',
    'جمادى الأولى', 'جمادى الآخرة', 'رجب', 'شعبان',
    'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
]
AR_NUMS = '٠١٢٣٤٥٦٧٨٩'

def to_ar_num(n: int) -> str:
    return ''.join(AR_NUMS[int(d)] for d in str(n))


DUAS = [
    ('﴿رَبَّنَا لَا تُؤَاخِذْنَا إِن نَّسِينَا أَوْ أَخْطَأْنَا﴾',
     'البقرة: ٢٨٦'),

    ('اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ',
     'سيد الاستغفار'),

    ('أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ',
     'حصن المسلم'),

    ('بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ',
     'حصن المسلم'),

    ('حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ',
     'التوبة: ١٢٩'),

    ('سُبْحَانَ اللَّهِ وَبِحَمْدِهِ سُبْحَانَ اللَّهِ الْعَظِيمِ',
     'حصن المسلم'),

    ('﴿لَا إِلَهَ إِلَّا أَنتَ سُبْحَانَكَ إِنِّي كُنتُ مِنَ الظَّالِمِينَ﴾',
     'الأنبياء: ٨٧'),

    ('اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ وَالْعَجْزِ وَالْكَسَلِ',
     'حصن المسلم'),

    ('﴿رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي﴾',
     'طه: ٢٥-٢٦'),

    ('اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالآخِرَةِ',
     'حصن المسلم'),

    ('﴿رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ﴾',
     'البقرة: ٢٠١'),

    ('يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ أَصْلِحْ لِي شَأْنِي كُلَّهُ',
     'حصن المسلم'),

    ('اللَّهُمَّ إِنِّي أَسْأَلُكَ الثَّبَاتَ فِي الْأَمْرِ وَالْعَزِيمَةَ عَلَى الرُّشْدِ',
     'حصن المسلم'),

    ('رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِن لَّدُنكَ رَحْمَةً',
     'آل عمران: ٨'),

    ('اللَّهُمَّ اغْفِرْ لِي وَلِوَالِدَيَّ وَلِلْمُؤْمِنِينَ يَوْمَ يَقُومُ الْحِسَابُ',
     'إبراهيم: ٤١'),
]


# ── Hijri date ────────────────────────────────────────────────────────────────
def get_hijri(date: datetime.date) -> dict:
    h = Gregorian(date.year, date.month, date.day).to_hijri()
    return {'d': h.day, 'm': h.month, 'y': h.year}


# ── Glass Card ────────────────────────────────────────────────────────────────
class GlassCard(FloatLayout):
    """A frosted-glass style card with rounded corners and highlight."""

    def __init__(self, radius=18, **kwargs):
        self._radius = radius
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.before.clear()
        r   = dp(self._radius)
        x, y        = self.x, self.y
        w, h        = self.width, self.height

        with self.canvas.before:
            # Outer shadow
            Color(0, 0, 0, 0.28)
            RoundedRectangle(pos=(x + dp(2), y - dp(3)), size=(w, h), radius=[r])

            # Glass body
            Color(1, 1, 1, 0.065)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[r])

            # Inner top gradient highlight
            Color(1, 1, 1, 0.13)
            RoundedRectangle(pos=(x + w*0.2, y + h - dp(1.5)),
                             size=(w * 0.6, dp(1.5)), radius=[dp(1)])

            # Border
            Color(1, 1, 1, 0.10)
            Line(rounded_rectangle=[x, y, w, h, r], width=dp(0.9))


# ── Analog Clock ──────────────────────────────────────────────────────────────
class AnalogClock(Widget):
    """Live analog clock drawn on Canvas, redrawn every second."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw)
        Clock.schedule_interval(self._redraw, 1)

    def _redraw(self, *_):
        self.canvas.clear()
        now = datetime.datetime.now()
        cx, cy = self.center_x, self.center_y
        R = min(self.width, self.height) / 2 - dp(5)

        with self.canvas:
            # Face background
            Color(1, 1, 1, 0.05)
            Ellipse(pos=(cx - R, cy - R), size=(R * 2, R * 2))

            # Face border
            Color(1, 1, 1, 0.14)
            Line(circle=(cx, cy, R), width=dp(1))

            # Tick marks
            for i in range(60):
                angle = math.radians(90 - i * 6)
                major = (i % 5 == 0)
                r1 = R - (dp(9) if major else dp(4))
                r2 = R - dp(1)
                Color(1, 1, 1, 0.55 if major else 0.18)
                Line(
                    points=[cx + math.cos(angle)*r1, cy + math.sin(angle)*r1,
                            cx + math.cos(angle)*r2, cy + math.sin(angle)*r2],
                    width=dp(1.5) if major else dp(0.7)
                )

            hr = now.hour % 12
            mn = now.minute
            sc = now.second

            # ── Hour hand ──
            ha = math.radians(90 - (hr + mn / 60) / 12 * 360)
            Color(1, 1, 1, 1)
            Line(points=[cx - math.cos(ha)*R*0.12, cy - math.sin(ha)*R*0.12,
                         cx + math.cos(ha)*R*0.50, cy + math.sin(ha)*R*0.50],
                 width=dp(2.8), cap='round')

            # ── Minute hand ──
            ma = math.radians(90 - (mn + sc / 60) / 60 * 360)
            Line(points=[cx - math.cos(ma)*R*0.12, cy - math.sin(ma)*R*0.12,
                         cx + math.cos(ma)*R*0.70, cy + math.sin(ma)*R*0.70],
                 width=dp(2.0), cap='round')

            # ── Second hand ──
            sa = math.radians(90 - sc / 60 * 360)
            Color(0.91, 0.25, 0.34, 1)
            Line(points=[cx - math.cos(sa)*R*0.18, cy - math.sin(sa)*R*0.18,
                         cx + math.cos(sa)*R*0.82, cy + math.sin(sa)*R*0.82],
                 width=dp(1.1), cap='round')

            # ── Center pin ──
            Color(0.91, 0.25, 0.34, 1)
            Ellipse(pos=(cx - dp(4.5), cy - dp(4.5)), size=(dp(9), dp(9)))
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx - dp(2.2), cy - dp(2.2)), size=(dp(4.4), dp(4.4)))


# ── Label factory ─────────────────────────────────────────────────────────────
def make_label(text='', size=sp(16), color=(1,1,1,.9), bold=False) -> Label:
    lbl = Label(
        text=ar(text) if text else '',
        font_size=size,
        color=color,
        bold=bold,
        halign='center',
        valign='middle',
    )
    lbl.bind(size=lambda l, v: setattr(l, 'text_size', (v[0], None)))
    return lbl


# ── Main Screen ───────────────────────────────────────────────────────────────
class WidgetScreen(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dua_idx = 0
        self._build()
        self._refresh()
        Clock.schedule_interval(lambda _: self._refresh(), 60)
        Clock.schedule_interval(lambda _: self._next_dua(), 12)

    # ── UI construction ───────────────────────────────────────────────────────
    def _build(self):
        root = BoxLayout(
            orientation='vertical',
            padding=[dp(14), dp(18), dp(14), dp(10)],
            spacing=dp(9),
            size_hint=(1, 1),
        )

        # ── Card 1 : Day name ────────────────────────────────────────────────
        c1 = GlassCard(size_hint=(1, None), height=dp(105))
        b1 = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(2))
        self.lbl_day       = make_label(size=sp(44), bold=True)
        self.lbl_greg_tiny = make_label(size=sp(11), color=(1,1,1,.38))
        b1.add_widget(self.lbl_day)
        b1.add_widget(self.lbl_greg_tiny)
        c1.add_widget(b1)
        root.add_widget(c1)

        # ── Card 2 : Gregorian month + day ───────────────────────────────────
        c2 = GlassCard(size_hint=(1, None), height=dp(88))
        b2 = BoxLayout(orientation='vertical', padding=dp(12))
        self.lbl_greg_big = make_label(size=sp(40), bold=True)
        b2.add_widget(self.lbl_greg_big)
        c2.add_widget(b2)
        root.add_widget(c2)

        # ── Card 3 : Hijri ───────────────────────────────────────────────────
        c3 = GlassCard(size_hint=(1, None), height=dp(72))
        b3 = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(3))
        lbl_htitle = make_label('التاريخ الهجري', size=sp(10), color=(1,1,1,.32))
        self.lbl_hijri = make_label(size=sp(20), bold=True)
        b3.add_widget(lbl_htitle)
        b3.add_widget(self.lbl_hijri)
        c3.add_widget(b3)
        root.add_widget(c3)

        # ── Card 4 : Dua ─────────────────────────────────────────────────────
        c4 = GlassCard(size_hint=(1, None), height=dp(108))
        b4 = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(5))
        self.lbl_dua     = make_label(size=sp(14.5), color=(1,1,1,.92))
        self.lbl_dua_src = make_label(size=sp(10),   color=(1,1,1,.28))
        lbl_tap          = make_label('اضغط للتغيير ↺', size=sp(9), color=(1,1,1,.18))
        b4.add_widget(self.lbl_dua)
        b4.add_widget(self.lbl_dua_src)
        b4.add_widget(lbl_tap)
        c4.add_widget(b4)
        c4.bind(on_touch_down=lambda w, t: w.collide_point(*t.pos) and self._next_dua())
        root.add_widget(c4)

        # ── Bottom row ───────────────────────────────────────────────────────
        row = BoxLayout(orientation='horizontal', spacing=dp(9),
                        size_hint=(1, None), height=dp(136))

        # Mini date
        c5 = GlassCard(size_hint=(1, 1))
        b5 = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(1))
        self.lbl_mwday  = make_label(size=sp(10),  color=(1,1,1,.38))
        self.lbl_mnum   = make_label(size=sp(40),  bold=True)
        self.lbl_mmonth = make_label(size=sp(10),  color=(1,1,1,.38))
        self.lbl_mhj    = make_label(size=sp(9.5), color=(1,1,1,.24))
        for w in [self.lbl_mwday, self.lbl_mnum, self.lbl_mmonth, self.lbl_mhj]:
            b5.add_widget(w)
        c5.add_widget(b5)
        row.add_widget(c5)

        # Clock
        c6 = GlassCard(size_hint=(1, 1))
        b6 = BoxLayout(orientation='vertical', padding=dp(6), spacing=dp(2))
        self.lbl_cwday = make_label(size=sp(10), color=(1,1,1,.32))
        self.clock     = AnalogClock(size_hint=(1, 1))
        b6.add_widget(self.lbl_cwday)
        b6.add_widget(self.clock)
        c6.add_widget(b6)
        row.add_widget(c6)

        root.add_widget(row)

        # ── Signature ────────────────────────────────────────────────────────
        sig = Label(
            text='By.Abdullah NassEr [color=e84057]♥[/color]',
            markup=True,
            font_size=sp(12),
            color=(1, 1, 1, 0.28),
            size_hint=(1, None),
            height=dp(26),
            halign='center',
        )
        root.add_widget(sig)

        self.add_widget(root)

    # ── Data refresh ─────────────────────────────────────────────────────────
    def _refresh(self, *_):
        now  = datetime.datetime.now()
        hj   = get_hijri(now.date())

        day_idx   = (now.weekday() + 1) % 7      # Python Mon=0 → Sun=0
        day_str   = AR_DAYS[day_idx]
        month_str = AR_MONTHS[now.month - 1]
        hj_str    = (f"{to_ar_num(hj['d'])} {HJ_MONTHS[hj['m']-1]} "
                     f"{to_ar_num(hj['y'])} هـ")
        greg_tiny = f"{now.year} / {now.month:02d} / {now.day:02d}"

        self.lbl_day.text       = ar(day_str)
        self.lbl_greg_tiny.text = greg_tiny
        self.lbl_greg_big.text  = ar(f"{to_ar_num(now.day)} {month_str}")
        self.lbl_hijri.text     = ar(hj_str)
        self.lbl_mwday.text     = ar(day_str)
        self.lbl_mnum.text      = ar(to_ar_num(now.day))
        self.lbl_mmonth.text    = ar(month_str)
        self.lbl_mhj.text       = ar(f"{to_ar_num(hj['d'])} {HJ_MONTHS[hj['m']-1]}")
        self.lbl_cwday.text     = ar(day_str)
        self._show_dua()

    def _show_dua(self):
        txt, src = DUAS[self._dua_idx]
        self.lbl_dua.text     = ar(txt)
        self.lbl_dua_src.text = ar(f"{src}  •  حصن المسلم")

    def _next_dua(self, *_):
        self._dua_idx = (self._dua_idx + 1) % len(DUAS)
        self._show_dua()


# ── App entry ─────────────────────────────────────────────────────────────────
class AbdullahNasserApp(App):
    def build(self):
        self.title = 'By.Abdullah NassEr'
        return WidgetScreen()


if __name__ == '__main__':
    AbdullahNasserApp().run()
