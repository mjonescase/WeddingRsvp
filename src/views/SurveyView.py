class SurveyView:
    @staticmethod
    def get_html(csrf_token: str) -> str:
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
            background: #222 url('https://s3-us-west-2.amazonaws.com/rsvp.adriandmikejones.com/beach.jpg') center center no-repeat;
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
                <div class="col-xl-8 col-lg-9 col-md-10 col-sm-12 mx-auto text-center form p-4">
                  <h3>We hope you'll join us in celebrating our first year of marriage<h3>
                  <p>Please come in your comfortable, casual clothes. The meal will be served at 2:00 pm, and alcoholic beverages will be available after 3:00 pm.</p>
                  <p>Saturday, September 12th, 1 - 6 pm</p>
                  <p>10280 Pearce Mill Rd, Allison Park, PA, 15101</p>
                  <div class="px-2">
                    <form action="/submitSurvey" class="justify-content-center" method="POST">
                      <div class="form-group">
                        <input type="hidden" id="csrf-token" name="csrf-token" value="{csrf_token}">
                        <label for="name">Please enter your name:</label>
                        <input type="text" maxlength="20" class="form-control" id="name" name="name">
                        <p>Will you be able to attend?</p>
                        <input type="radio" class="form-control" id="Yes" name="attending">
                        <label for="Yes">Yes, I will be there.</label>
                        <input type="radio" class="form-control" id="No" name="attending">
                        <label for="No">I regret that I am unable to attend.</label>
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
