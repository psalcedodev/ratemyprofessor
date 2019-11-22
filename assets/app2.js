var professors_info = document.querySelector(".professors_info");
function show_my_professors() {
  fetch("http://localhost:8080/professors", { credentials: "include" }).then(
    function(response) {
      response.json().then(function(data) {
        //Loops for data in our txt file
        professors_info.innerHTML = "";
        data.forEach(function(professor) {
          //Creates a div with a classname called Column

          var column = document.createElement("div");
          column.className = "column";
          professors_info.appendChild(column);
          //Creates a div with a classname called Column_row appending it to Column
          var column_row = document.createElement("div");
          column_row.className = "column_row";
          column.appendChild(column_row);
          //Creates a div with a classname called prof_des appending it to Column_row
          var prof_des = document.createElement("div");
          prof_des.className = "prof_des";
          column_row.appendChild(prof_des);
          //Creates a div with a classname called Column_left appending it to Column
          var column_left = document.createElement("div");
          column_left.className = "column_left";
          column.appendChild(column_left);
          //Creates a div with a classname called Column_right appending it to Column
          var column_right = document.createElement("div");
          column_right.className = "column_right";
          column.appendChild(column_right);

          //Professor's First and Last name
          var full_name = document.createElement("h4");
          full_name.innerHTML =
            professor.first_name + " " + professor.last_name;
          prof_des.appendChild(full_name);

          //Professor's department
          var department = document.createElement("h5");
          department.innerHTML = professor.department;
          prof_des.appendChild(department);

          //Creates the field for options

          var options = document.createElement("div");
          options.className = "menu";
          options.id = "menu";
          options.innerHTML = '<i class="fas fa-ellipsis-v"></i>';
          var options_list = document.createElement("div");
          options_list.className = "sub_menu";
          options.appendChild(options_list);
          options.onclick = function() {
            if (options_list.style.display === "none") {
              options_list.style.display = "block";
            } else {
              options_list.style.display = "none";
            }
          };
          column_row.appendChild(options);
          //Rate Buttons

          var rate_buttons = document.createElement("div");
          rate_buttons.className = "rate_buttons";
          column_right.appendChild(rate_buttons);
          // function getSession() {
          //   fetch("http://localhost:8080/sessions", {
          //     credentials: "include"
          //   }).then(function(response) {
          //     if (response.status == 404) {

          //     } else {

          //     }
          //   });
          // }

          // getSession();
          //Shows Overall Average Rating
          function show_avg() {
            fetch(
              "http://localhost:8080/professor/rating/avg/" +
                professor.professor_id,
              { credentials: "include" }
            ).then(function(response) {
              response.json().then(function(data) {
                var rate = data.rating;
                var overall_text = document.createElement("h3");
                overall_text.innerHTML = "Overall Rating";
                overall_text.className = "overall_rating_text";
                column_left.appendChild(overall_text);
                var rate_value = document.createElement("h4");
                rate_value.className = "overall_rating";
                if (rate !== null) {
                  var num_total = rate.toFixed(2);
                  rate_value.innerHTML = num_total;
                } else {
                  rate_value.innerHTML = "N/A";
                }
                column_left.appendChild(rate_value);
              });
            });
          }
          show_avg();
          //Shows an AVG of difficulty
          function show_difficulty() {
            fetch(
              "http://localhost:8080/professor/rating/difficulty/" +
                professor.professor_id,
              { credentials: "include" }
            ).then(function(response) {
              response.json().then(function(data) {
                var dif = data.difficulty;
                var difficulty_text = document.createElement("h3");
                difficulty_text.innerHTML = "Difficulty";
                difficulty_text.className = "overall_difficulty_text";
                column_left.appendChild(difficulty_text);
                //Value
                var difficult = document.createElement("h4");
                difficult.className = "overall_rating";
                if (dif !== null) {
                  var num_total = dif.toFixed(2);
                  difficult.innerHTML = num_total;
                } else {
                  difficult.innerHTML = "N/A";
                }
                column_left.appendChild(difficult);
              });
            });
          }
          show_difficulty();
          //Shows ratings for each professor
          var show_rating = document.createElement("button");
          show_rating.innerHTML = "Show Ratings";
          rate_buttons.appendChild(show_rating);

          show_rating.onclick = function() {
            fetch("http://localhost:8080/ratings/" + professor.professor_id, {
              credentials: "include"
            }).then(function(response) {
              response.json().then(function(data) {
                var main_page = document.querySelector("#main_page");
                var overlay_show_ratings = document.createElement("div");
                overlay_show_ratings.id = "overlay_show_ratings";
                main_page.appendChild(overlay_show_ratings);
                data.forEach(function(rating) {
                  document.querySelector(
                    "#overlay_show_ratings"
                  ).style.display = "block";
                  var professor_ratings = document.createElement("div");
                  professor_ratings.id = "professor_ratings";
                  overlay_show_ratings.appendChild(professor_ratings);

                  var rating_box = document.createElement("div");
                  rating_box.className = "rating_box";
                  professor_ratings.appendChild(rating_box);
                  //First Column of rating details
                  var rating_details = document.createElement("div");
                  rating_details.className = "rating_details";
                  rating_box.appendChild(rating_details);

                  //Second Column of rating details
                  var class_details = document.createElement("div");
                  class_details.className = "class_details";
                  rating_box.appendChild(class_details);
                  //Third Column of rating details
                  var rating_comment = document.createElement("div");
                  rating_comment.className = "rating_comment";
                  rating_box.appendChild(rating_comment);

                  //Shows prof Class quality
                  var prof_quality = document.createElement("h4");
                  prof_quality.innerHTML = rating.rating;
                  rating_details.appendChild(prof_quality);
                  //Shows prof Class Difficulty
                  var prof_difficulty = document.createElement("h4");
                  prof_difficulty.innerHTML = rating.difficulty;
                  rating_details.appendChild(prof_difficulty);

                  //Show class course
                  var prof_course = document.createElement("h5");
                  prof_course.innerHTML = "Course: " + rating.course;
                  class_details.appendChild(prof_course);
                  //Shows if Attendance was important
                  var prof_attendance = document.createElement("h5");
                  prof_attendance.innerHTML =
                    "Attendance: " + rating.attendance;
                  class_details.appendChild(prof_attendance);
                  //Shows if the prof used a textbook in his class
                  var prof_textbook = document.createElement("h5");
                  prof_textbook.innerHTML = "Textbook Used: " + rating.textbook;
                  class_details.appendChild(prof_textbook);
                  //Shows if the student would take the professor's class again
                  var prof_retake = document.createElement("h5");
                  prof_retake.innerHTML = "Would take again: " + rating.retake;
                  class_details.appendChild(prof_retake);

                  //Shows student's grade received
                  var prof_grade = document.createElement("h5");
                  prof_grade.innerHTML = "Grade Received: " + rating.grade;
                  class_details.appendChild(prof_grade);

                  //Shows the student's comment about the professor
                  var prof_comment = document.createElement("h5");
                  prof_comment.innerHTML = rating.comment;
                  rating_comment.appendChild(prof_comment);
                });
              });
            });
          };

          /*Post Rating*/
          var rating = document.createElement("button");
          rating.innerHTML = "Rate";
          rating.id = "rate_button";
          rate_buttons.appendChild(rating);
          rating.onclick = function() {
            var show_prof = document.querySelector("#title_prof");
            show_prof.innerHTML =
              professor.first_name + " " + professor.last_name;

            document.querySelector("#overlay_rating").style.display = "block";

            var RateButton = document.querySelector("#add_rating");

            RateButton.onclick = function() {
              var course = document.querySelector("#course").value;
              var rating = document.querySelector("#rating");

              var value_rate = rating.options[rating.selectedIndex].value;
              var difficulty = document.querySelector("#difficulty");

              var value_dif =
                difficulty.options[difficulty.selectedIndex].value;
              var retake = document.querySelector("#retake");

              var value_retake = retake.options[retake.selectedIndex].value;
              var textbook = document.querySelector("#textbook");

              var value_text = textbook.options[textbook.selectedIndex].value;
              var attendance = document.querySelector("#attendance");
              var value_atten =
                attendance.options[attendance.selectedIndex].value;
              var grade = document.querySelector("#grade");

              var value_grade = grade.options[grade.selectedIndex].value;

              var comment = document.querySelector("#comment").value;
              document.querySelector("#course").innerHTML = "";

              document.querySelector("#rating").value = "";

              document.querySelector("#difficulty").value = "";

              document.querySelector("#retake").value = "";

              document.querySelector("#textbook").value = "";

              document.querySelector("#attendance").value = "";

              document.querySelector("#grade").value = "";
              document.querySelector("#comment").innerHTML = "";
              var body = "course=" + encodeURIComponent(course);
              body += "&rating=" + encodeURIComponent(value_rate);
              body += "&difficulty=" + encodeURIComponent(value_dif);
              body += "&retake=" + encodeURIComponent(value_retake);
              body += "&textbook=" + encodeURIComponent(value_text);
              body += "&attendance=" + encodeURIComponent(value_atten);
              body += "&grade=" + encodeURIComponent(value_grade);
              body += "&comment=" + encodeURIComponent(comment);
              fetch("http://localhost:8080/ratings/" + professor.professor_id, {
                method: "POST",
                body: body,
                credentials: "include",
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
              }).then(function(response) {
                document.querySelector("#overlay_rating").style.display =
                  "none";
                show_my_professors();
              });
            };
          };

          /*UPDATE*/
          var update = document.createElement("li");
          update.innerHTML = "Update";
          update.id = "update_button";
          options_list.appendChild(update);
          update.onclick = function() {
            document.querySelector("#overlay_update").style.display = "block";

            //prefill form here

            document.querySelector("#f_name").value = professor.first_name;

            document.querySelector("#l_name").value = professor.last_name;

            document.querySelector("#dept").value = professor.department;

            document.querySelector("#direct").value = professor.directory;
            var UpdateButton = document.querySelector("#update");

            UpdateButton.onclick = function() {
              UpdateProfessor(professor.professor_id);
            };
          };
          /*DELETE*/
          var DeleteButton = document.createElement("li");
          DeleteButton.innerHTML = "Delete";
          DeleteButton.id = "delete_button";
          options_list.appendChild(DeleteButton);
          DeleteButton.onclick = function() {
            if (
              confirm(
                "Are you sure you want to delete professor " +
                  professor.first_name +
                  " " +
                  professor.last_name +
                  "?"
              )
            ) {
              DeleteProfessor(professor.professor_id);
            }
          };
        });
      });
    }
  );
}
show_my_professors();

var DeleteProfessor = function(professorId) {
  fetch("http://localhost:8080/professors/" + professorId, {
    method: "DELETE",
    credentials: "include"
  }).then(function(response) {
    show_my_professors();
  });
};
var UpdateProfessor = function(professorid) {
  var first_name = document.querySelector("#f_name").value;
  var last_name = document.querySelector("#l_name").value;
  var department = document.querySelector("#dept").value;
  var directory = document.querySelector("#direct").value;
  document.querySelector("#f_name").value = "";
  document.querySelector("#l_name").value = "";
  document.querySelector("#dept").value = "";
  document.querySelector("#direct").value = "";
  var body = "f_name=" + encodeURIComponent(first_name);
  body += "&l_name=" + encodeURIComponent(last_name);
  body += "&dept=" + encodeURIComponent(department);
  body += "&direct=" + encodeURIComponent(directory);
  fetch("http://localhost:8080/professors/" + professorid, {
    // request parameters:
    method: "PUT",
    body: body,
    credentials: "include",
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  }).then(function(response) {
    // handle the response:

    document.querySelector("#overlay_update").style.display = "none";
    show_my_professors();
  });
};

var registerButton = document.querySelector("#register");
registerButton.onclick = function() {
  var firstName = document.querySelector("#firstName").value;
  var lastName = document.querySelector("#lastName").value;
  var email = document.querySelector("#email").value;
  var pwd = document.querySelector("#pwd").value;
  //Clears all values
  document.querySelector("#firstName").value = "";
  document.querySelector("#lastName").value = "";
  document.querySelector("#email").value = "";
  document.querySelector("#pwd").value = "";
  var body = "firstName=" + encodeURIComponent(firstName);
  body += "&lastName=" + encodeURIComponent(lastName);
  body += "&email=" + encodeURIComponent(email);
  body += "&passwd=" + encodeURIComponent(pwd);
  fetch("http://localhost:8080/users", {
    // request parameters:
    method: "POST",
    body: body,
    credentials: "include",
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  }).then(function(response) {
    if (response.status == 422) {
      console.log("422");
      alert("Email already in use. Please try to log in");
      document.querySelector("#overlay_login").style.display = "block";
    } else {
      alert("Thank you for registering");
    }
    document.querySelector("#overlay_register").style.display = "none";
  });
};

var loginButton = document.querySelector("#login");
loginButton.onclick = function() {
  var email = document.querySelector("#log_email").value;
  var pwd = document.querySelector("#log_pass").value;
  document.querySelector("#log_email").value = "";
  document.querySelector("#log_pass").value = "";
  var body = "&email=" + encodeURIComponent(email);
  body += "&passwd=" + encodeURIComponent(pwd);
  fetch("http://localhost:8080/sessions", {
    // request parameters:
    method: "POST",
    body: body,
    credentials: "include",
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  }).then(function(response) {
    if (response.status == 201) {
      alert("Welcome " + email);
      document.querySelector("#loginTop").style.display = "none";
      document.querySelector("#acc_info").style.display = "block";
      document.querySelector("#add_professor").style.display = "block";
      document.querySelector("#username_show").innerHTML = email;
    } else {
      alert("Your username/password is incorrect. Please try again");
    }
    document.querySelector("#overlay_login").style.display = "none";
  });
};
//Adds a professor
var addButton = document.querySelector("#add");
addButton.onclick = function() {
  var first_name = document.querySelector("#first_name").value;
  var last_name = document.querySelector("#last_name").value;
  var department = document.querySelector("#department").value;
  var directory = document.querySelector("#directory").value;
  document.querySelector("#first_name").value = "";
  document.querySelector("#last_name").value = "";
  document.querySelector("#department").value = "";
  document.querySelector("#directory").value = "";
  var body = "first_name=" + encodeURIComponent(first_name);
  body += "&last_name=" + encodeURIComponent(last_name);
  body += "&department=" + encodeURIComponent(department);
  body += "&directory=" + encodeURIComponent(directory);
  fetch("http://localhost:8080/professors", {
    // request parameters:
    method: "POST",
    body: body,
    credentials: "include",

    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  }).then(function(response) {
    document.querySelector("#overlay_add").style.display = "none";
    show_my_professors();
  });
};

function on_add() {
  document.querySelector("#overlay_add").style.display = "block";
}
function off_add() {
  document.querySelector("#overlay_add").style.display = "none";
}

function off_rate() {
  document.querySelector("#overlay_rating").style.display = "none";
}
function off_update() {
  document.querySelector("#overlay_update").style.display = "none";
}
function on_login() {
  document.querySelector("#overlay_login").style.display = "block";
}
function off_login() {
  document.querySelector("#overlay_login").style.display = "none";
}

function on_register() {
  document.querySelector("#overlay_register").style.display = "block";
}
function off_register() {
  document.querySelector("#overlay_register").style.display = "none";
}
