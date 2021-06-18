This repository documents my setup for qutebrowser and i3 that combines qb's
`tabs.tabs_are_windows` option with i3's tabbed layout. The main advantages of
this setup are that tabs can be moved freely to different workspaces or put
side-by-side, without having to reload them (such as with `tab-give`). And the
tabs can be mixed with other applications such as a PDF-reader.

On the other hand, `tabs_are_windows` has several shortcomings, many of which I
have circumvented with some more or less hacky solutions:

1. **Focusing tabs**: Obviously, qb's commands to switch tabs don't
   work on i3 tabs. Instead, you can use i3's bindings.
   Due to muscle memory, I have also bound the following in qb itself:

        config.bind(']', 'spawn ~/.local/share/i3/window-tool tab-focus next')
        config.bind('[', 'spawn ~/.local/share/i3/window-tool tab-focus prev')
        config.bind('}', 'spawn ~/.local/share/i3/window-tool tab-move next')
        config.bind('{', 'spawn ~/.local/share/i3/window-tool tab-move prev')

   Here, I'm using a script from my
   [i3-tools](https://github.com/miseran/i3-tools), but of course, you could
   simply use `i3-msg focus right` etc.

2. **Closing the last tab**: To simulate the setting `tabs.last_close =
   'default-page'`, which keeps a qb window open when the last tab is closed, I
   use the userscript `tab-close` in this repo (requires
   [jq](https://github.com/stedolan/jq)). It's not perfect though, especially
   with respect to `undo`.

        config.bind('q', 'spawn --userscript tab-close')

3. **Background tabs**: qb has no control over whether i3 focuses a newly
   created tab, so all new tabs will open in the foreground. This can be
   circumvented by a hack that sets the `WM_WINDOW_ROLE` of background tabs
   differently (see [here](https://github.com/qutebrowser/qutebrowser/issues/3819)).
   Then, you can tell i3 to not focus these tabs when they open:

        no_focus [window_role="^qutebrowser_background$"]

   Instead of patching qb directly, I added a horrible monkey patch to
   `config.py`.

4. **Tabbing new windows**: I use an i3 workspace layout and a custom desktop
   file to open new qb windows in a tabbed layout, but only if the
   current workspace is empty. See the script, layout and desktop file
   `qutebrowser-layout.*` (requires jq).

5. **Favicons**: In the very freshest builds of i3, you can even show favicons
   in the tab bar! You just need to enable it in i3's config.

        for_window [class=".*"] title_window_icon on

6. **Always showing the tab bar**: Since I disable i3's title bars in regular
   windows, a tabbed container with a single child will not display a tab bar
   either. My feature request to make this configurable was rejected, so I had
   no choice but to patch i3 myself to always show a tab bar in a tabbed
   container. See the file `i3_patch`.

   As a bonus, the patch does the opposite for stacked containers: It never
   shows the titlebar, kind of like herbstluftwm's maximized layout. I mostly
   use this to hide a terminal that launches a gui app behind that app's window.
   And I was never using the old stacked layout anyway.

7. **Opening qb tabs from other applications**: If another application opens a
   qb window, it will open next to that instead of with the existing tabs, which
   is not always what I want. This can be circumvented by telling i3 to open all
   new qb windows on a given workspace, but I chose not to do that, since
   sometimes it's preferable to keep the new window where it is. Instead, I
   simply made a binding:

        config.bind('z', 'spawn i3-msg move container to workspace 2, workspace 2')
