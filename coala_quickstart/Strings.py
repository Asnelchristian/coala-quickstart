logo_string = """
  .o88Oo._
 d8P         .ooOO8bo._
 88                  '*Y8bo.
 YA                      '*Y8b   __
  YA                        68o68**8Oo.
   "8D                       *"'    "Y8o
    Y8     'YB                       .8D
    '8               d8'             8D
     8       d8888b          d      AY
     Y,     d888888         d'  _.oP"
      q.    Y8888P'        d8
       "q.  `Y88P'       d8"
          Y           ,o8P
               oooo888P"
"""
coala_bear_logo = logo_string.split("\n")

welcome_messages = ["Hi there! Awesome you decided to do some high "
                    "quality coding. coala is just the tool you need!",

                    "You can configure coala to suit your needs. This "
                    "is done with a settings file called a `.coafile` "
                    "in the project directory.",

                    "We can help you with that. Let's get started with "
                    "some basic questions."]


glob_help_url = "http://coala.readthedocs.io/en/latest/Users/Glob_Patterns.html"
glob_help = """
File globs are a very concise way to specify a large
number of files. You may give multiple file globs
separated by commas. To learn more about glob patterns
please visit: {}

For example, you may want to include your src/ folder and
all its contents but exclude your .git directory and all
.o files. To do this, simply give `src/` for the first
question and `.git/**,**/*.o` for the second question.
""".format(glob_help_url)
