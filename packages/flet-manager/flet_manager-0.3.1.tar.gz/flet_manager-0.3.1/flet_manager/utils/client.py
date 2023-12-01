#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from ast import literal_eval
from urllib.parse import urlparse, parse_qsl

from flet_core import Page, RouteChangeEvent

from .themes import Themes


class Client:
    page: Page
    routes: dict
    view_main = None
    view_error = None
    session: None

    def __init__(
            self,
            page: Page,
            themes: Themes,
            fonts: dict,
            routes,
            view_main,
            view_error,
    ):
        self.page = page
        self.routes = routes
        self.view_main = view_main
        self.view_error = view_error

        self.page.fonts = fonts
        self.page.theme, self.page.dark_theme = themes.get()

        self.page.on_view_pop = self.pop_view
        self.page.on_route_change = self.change_route
        self.page.views.clear()

    async def pop_view(self, _):
        await self.change_view(go_back=True)

    async def change_view(
            self,
            view=None,
            go_back: bool = False,
    ):
        if go_back:
            self.page.views.pop()

        if not self.page.views and not view:
            view = self.view_main()
        if view:
            view.client = self
            await view.build()
            self.page.views.append(await view.get())

        # Change title & update
        if view:
            self.page.title = view.title
        else:
            self.page.title = self.page.views[-1].title

        await self.page.go_async(self.page.views[-1].route)
        await self.page.update_async()

    async def change_route(self, e: RouteChangeEvent):
        url = urlparse(e.route)
        route = url.path
        params = {}

        # Set params for view
        for key, value in dict(parse_qsl(url.query)).items():
            try:
                value = literal_eval(str(value))
            except ValueError:
                pass
            params[key] = value
        if self.page.views[-1].route == e.route:
            return

        # Go back if current == -2 view
        try:
            if self.page.views[-2].route == e.route:
                return await self.change_view(go_back=True)
        except IndexError:
            pass

        try:
            view = self.routes[route]
        except KeyError:
            view = self.view_error
            params['error_code'] = 404
        await self.change_view(view=view(**params))

    async def change_themes(self, themes: Themes):
        self.page.theme, self.page.dark_theme = themes.get()
        await self.page.update_async()
