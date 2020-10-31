# Trick-or-treat table lightpack client

The great coronavirus pandemic of 2020 necessitated any Halloween-night fun be kept totally contactless. Having a spare
[Lightpack](https://lightpack.tv/) sitting around, as well as an IKEA kitchen table made of white frosted glass, I
decided to make an interactive trick-or-treat distribution point that you could change the color of by interacting with
a website.

It's extremely simple and not built with much resilience, mostly because it only needs to work for about a 3 hour window
on Halloween evening.

## `trickortreat.html`

Front-end, uses `fetch()` to send requests.

## `lightpack_ctl.py`

Flask application that maintains a persistent connection to the Lightpack server on the laptop sitting at the end of the
driveway. (It's an old X220 Tablet from 2012, not really worth snatching, and my neighborhood is pretty safe anyways.)

## `.htaccess`

* GET requests go to the html
* POST requests are proxied to the flask app

## License

WTFPL.