# Flask-Phrase

**Flask-Phrase** is the official library for integrating [Phrase Strings In-Context Editor](https://support.phrase.com/hc/en-us/articles/5784095916188-In-Context-Editor-Strings) with [Flask](https://flask.palletsprojects.com/en/3.0.x/)

## :scroll: Documentation

### Prerequisites

To use Flask-Phrase with your application you have to:

- Sign up for a Phrase account: [https://app.phrase.com/signup](https://app.phrase.com/signup)
- Use the [Flask](https://flask.palletsprojects.com/en/3.0.x/) framework for Python

### Demo

You can find a demo project in the `demo` folder, just run follow the `README.md` in that folder

### Installation

#### NOTE: You can not use the old version of the ICE with integration versions of >2.0.0, you have to instead use 1.x.x versions as before

#### via pip

```bash
pip install Flask-Phrase
```

#### Configure

Add the following to your Flask app configuration (app.config or config.py file)

    PHRASEAPP_ENABLED = True
    PHRASEAPP_PREFIX = '{{__'
    PHRASEAPP_SUFFIX = '__}}'

Your app code should look something like this:

    from flask import Flask, [...]
    from flask_babel import Babel
    from flask_phrase import Phrase, gettext, ngettext
    app = Flask(__name__)
    babel = Babel(app)
    phrase = Phrase(app)

Last step: add the Phrase JavaScript snippet to your base layout file with the following tag. This should go inside the <head> section of your template file:

    <script>
        window.PHRASEAPP_CONFIG = {
            projectId: "YOUR-PROJECT-ID",
            accountId: "YOUR-ACCOUNT-ID",
            datacenter: "eu",
            origin: "Flask-Phrase"
        };
        (function() {
            var phrasejs = document.createElement('script');
            phrasejs.type = 'module';
            phrasejs.async = true;
            phrasejs.src = 'https://d2bgdldl6xit7z.cloudfront.net/latest/ice/index.js'
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(phrasejs, s);
        })();
    </script>

You can find your Project-ID and Account-ID in the Phrase Translation Center.

Old version of the ICE is not available since version 2.0.0. If you still would rather use the old version, please go back to 1.x.x versions.

#### Using the US Datacenter with ICE

In addition to `projectId` and `accountId` in the config, also add the US specific datacenter setting to enable working through the US endpoint.

```
window.PHRASEAPP_CONFIG = {
    projectId: "YOUR-PROJECT-ID",
    accountId: "YOUR-ACCOUNT-ID",
    datacenter: "us",
    origin: "Flask-Phrase"
};
```

### How does it work

Set the `PHRASEAPP_ENABLED` to `True/False` to enable or disable In-Context-Editing. When set to False, it will fall back to standard Flask-Babel's gettext functions. Disable Phrase for production environments at any time!

When `PHRASEAPP_ENABLED = True` this package modifies the returning values from translation functions to present a format which the ICE can read.

Flask-Phrase provides In-Context translating facilities to your Flask app by hooking into [flask-babel's](https://pypi.org/project/flask-babel/) gettext function. It exposes the underlying key names to the JavaScript editor that is provided by Phrase.

### Test

Run unit tests:

```bash
python manage.py test
```

## :white_check_mark: Commits & Pull Requests

We welcome anyone who wants to contribute to our codebase, so if you notice something, feel free to open a Pull Request! However, we ask that you please use the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for your commit messages and titles when opening a Pull Request.

Example: `chore: Update README`

## :question: Issues, Questions, Support

Please use [GitHub issues](https://github.com/phrase/Flask-Phrase/issues) to share your problem, and we will do our best to answer any questions or to support you in finding a solution.

## :books: Resources

- [Step-by-Step Guide on Flask-Babel and Flask-Phrase](https://phrase.com/blog/posts/python-localization-for-flask-applications/)
- [Flask-Phrase Demo Application](https://github.com/phrase/flask-demo-application/).
- [Localization Guides and Software Translation Best Practices](http://phrase.com/blog/)
- [Contact Phrase Team](https://phrase.com/en/contact)

## :memo: Changelog

Detailed changes for each release are documented in the [changelog](https://github.com/phrase/Flask-Phrase/releases).
