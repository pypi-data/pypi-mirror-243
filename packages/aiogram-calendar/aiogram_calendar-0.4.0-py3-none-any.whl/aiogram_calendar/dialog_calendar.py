import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

from .schemas import DialogCalendarCallback, DialogCalAct
from .common import GenericCalendar


class DialogCalendar(GenericCalendar):

    ignore_callback = DialogCalendarCallback(act=DialogCalAct.ignore).pack()    # placeholder for no answer buttons

    async def _get_month_kb(self, year: int):
        "Creates a inline keyboard with months for specified year"
        kb = []
        # first row with year button
        years_row = []
        years_row.append(
            InlineKeyboardButton(
                text=self._labels.cancel_caption,
                callback_data=DialogCalendarCallback(act=DialogCalAct.cancel, year=year, month=1, day=1).pack()
            )
        )
        years_row.append(InlineKeyboardButton(
            text=str(year),
            callback_data=DialogCalendarCallback(act=DialogCalAct.start, year=year, month=-1, day=-1).pack()
        ))
        years_row.append(InlineKeyboardButton(text=" ", callback_data=self.ignore_callback))
        kb.append(years_row)
        # two rows with 6 months buttons
        month6_row = []
        for month in self._labels.months[0:6]:
            month6_row.append(InlineKeyboardButton(
                text=month,
                callback_data=DialogCalendarCallback(
                    act=DialogCalAct.set_m, year=year, month=self._labels.months.index(month) + 1, day=-1
                ).pack()
            ))
        month12_row = []
        for month in self._labels.months[6:12]:
            month12_row.append(InlineKeyboardButton(
                text=month,
                callback_data=DialogCalendarCallback(
                    act=DialogCalAct.set_m, year=year, month=self._labels.months.index(month) + 1, day=-1
                ).pack()
            ))
        kb.append(month6_row)
        kb.append(month12_row)
        return InlineKeyboardMarkup(row_width=6, inline_keyboard=kb)

    async def _get_days_kb(self, year: int, month: int):
        "Creates a inline keyboard with calendar days of month for specified year and month"
        kb = []
        nav_row = []
        nav_row.append(
            InlineKeyboardButton(
                text=self._labels.cancel_caption,
                callback_data=DialogCalendarCallback(act=DialogCalAct.cancel, year=year, month=1, day=1).pack()
            )
        )
        nav_row.append(InlineKeyboardButton(
            text=str(year),
            callback_data=DialogCalendarCallback(act=DialogCalAct.start, year=year, month=-1, day=-1).pack()
        ))
        nav_row.append(InlineKeyboardButton(
            text=self._labels.months[month - 1],
            callback_data=DialogCalendarCallback(act=DialogCalAct.set_y, year=year, month=-1, day=-1).pack()
        ))
        kb.append(nav_row)

        week_days_labels_row = []
        for day in self._labels.days_of_week:
            week_days_labels_row.append(InlineKeyboardButton(text=day, callback_data=self.ignore_callback))
        kb.append(week_days_labels_row)

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            days_row = []
            for day in week:
                if (day == 0):
                    days_row.append(InlineKeyboardButton(text=" ", callback_data=self.ignore_callback))
                    continue
                days_row.append(InlineKeyboardButton(
                    text=str(day),
                    callback_data=DialogCalendarCallback(act=DialogCalAct.day, year=year, month=month, day=day).pack()
                ))
            kb.append(days_row)
        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)

    async def start_calendar(
        self,
        year: int = datetime.now().year,
        month: int = None
    ) -> InlineKeyboardMarkup:
        if month:
            return await self._get_days_kb(year, month)
        kb = []
        # inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        years_row = []
        for value in range(year - 2, year + 3):
            years_row.append(InlineKeyboardButton(
                text=str(value),
                callback_data=DialogCalendarCallback(act=DialogCalAct.set_y, year=value, month=-1, day=-1).pack()
            ))
        kb.append(years_row)
        # nav buttons
        nav_row = []
        nav_row.append(InlineKeyboardButton(
            text='<<',
            callback_data=DialogCalendarCallback(act=DialogCalAct.prev_y, year=year, month=-1, day=-1).pack()
        ))
        nav_row.append(InlineKeyboardButton(
            text=self._labels.cancel_caption,
            callback_data=DialogCalendarCallback(act=DialogCalAct.cancel, year=year, month=1, day=1).pack()
        ))
        nav_row.append(InlineKeyboardButton(
            text='>>',
            callback_data=DialogCalendarCallback(act=DialogCalAct.next_y, year=year, month=1, day=1).pack()
        ))
        kb.append(nav_row)
        return InlineKeyboardMarkup(row_width=5, inline_keyboard=kb)

    async def process_selection(self, query: CallbackQuery, data: DialogCalendarCallback) -> tuple:
        return_data = (False, None)
        if data.act == DialogCalAct.ignore:
            await query.answer(cache_time=60)
        if data.act == DialogCalAct.set_y:
            await query.message.edit_reply_markup(reply_markup=await self._get_month_kb(int(data.year)))
        if data.act == DialogCalAct.prev_y:
            new_year = int(data.year) - 5
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(year=new_year))
        if data.act == DialogCalAct.next_y:
            new_year = int(data.year) + 5
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(year=new_year))
        if data.act == DialogCalAct.start:
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(data.year)))
        if data.act == DialogCalAct.set_m:
            await query.message.edit_reply_markup(reply_markup=await self._get_days_kb(int(data.year), int(data.month)))
        if data.act == DialogCalAct.day:
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, datetime(int(data.year), int(data.month), int(data.day))
        if data.act == DialogCalAct.cancel:
            await query.message.delete_reply_markup()
        return return_data
