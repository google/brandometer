/*
Copyright 2019 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package brandometer;

import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;
import java.util.UUID;
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Brandometer survey response reveiver Logs GeoInformation of the requests for Reporting purpose
 * on BigQuery
 */
public class ResponseReceiver extends HttpServlet {

  public static final String BOM_COOKIE_NAME = "bomcook";
  public static final Integer BOM_COOKIE_EXPIRY = 365 * 24 * 60 * 60; // 1 Year In Seconds

  @Override
  protected void doGet(HttpServletRequest req, HttpServletResponse resp)
      throws ServletException, IOException {
    String country = req.getHeader("X-AppEngine-Country");
    String region = req.getHeader("X-AppEngine-Region");
    String city = req.getHeader("X-AppEngine-City");

    log(country + "/" + region + "/" + city);

    // Get the cookie or set

    Cookie bomCookie =
        Arrays.stream(Optional.ofNullable(req.getCookies()).orElse(new Cookie[] {}))
            .filter(cookie -> cookie.getName().equals(BOM_COOKIE_NAME))
            .findFirst()
            .orElse(new Cookie(BOM_COOKIE_NAME, UUID.randomUUID().toString()));

    log("bomcookie=" + bomCookie.getValue() + ";");

    // Set the cookie with new expiry
    bomCookie.setMaxAge(BOM_COOKIE_EXPIRY);
    resp.addCookie(bomCookie);
    resp.setStatus(204);
    return;
  }
}
