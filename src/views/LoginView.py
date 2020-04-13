from enum import Enum

class FailureReason(Enum):
    PASSCODE = "passcode"
    TIMEOUT = "timeout"

class LoginView:
    @staticmethod
    def get_html(
            csrf_token: str,
            failure_reason: FailureReason = None
    ) -> str:
        error_message: str = {
            FailureReason.PASSCODE: '<h3 class="py-2 text-truncate error">Invalid Passcode.</h3>',
            FailureReason.TIMEOUT: '<h3 class="py-2 text-truncate error">Form timed out. Please try again.</h3>'
        }.get(failure_reason, "")
        return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <title>RSVP</title>
        <style>
          #cover {{
            background: #222 url('https://s3-us-west-2.amazonaws.com/rsvp.adriandmikejones.com/background.jpg') center center no-repeat;
            background-size: cover;
            height: 100%;
            text-align: center;
            display: flex;
            align-items: center;
            position: relative;
          }}

          #cover-caption {{
              width: 100%;
              position: relative;
              z-index: 1;
          }}

          /* only used for background overlay not needed for centering */
          form:before {{
              content: '';
              height: 100%;
              left: 0;
              position: absolute;
              top: 0;
              width: 100%;
              background-color: rgba(0,0,0,0.3);
              z-index: -1;
              border-radius: 10px;
          }}

          .error {{
              color: red;
          }}
        </style>
      </head>
      <body>
        <section id="cover" class="min-vh-100">
          <div id="cover-caption">
            <div class="container">
              <div class="row text-white">
                <div class="col-xl-5 col-lg-6 col-md-8 col-sm-10 mx-auto text-center form p-4">
                  { error_message }
                  <h1 class="display-4 py-2 text-truncate">Passcode:</h1>
                  <div class="px-2">
                    <form action="/authenticate" class="justify-content-center" method="POST">
                      <div class="form-group">
                        <input type="hidden" id="csrf-token" name="csrf-token" value="{csrf_token}">
                        <input type="password" maxlength="20" class="form-control" id="passcode" name="passcode">
                      </div>
                        <input type="submit" class="btn btn-primary" value="Submit">
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </body>
    </html>
    """
