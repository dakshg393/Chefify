// base.html js


function toggleTheme() {
    var body = document.body;
    body.classList.toggle('dark-mode');

    // Store the current theme mode preference in a cookie
    var themeMode = body.classList.contains('dark-mode') ? 'dark' : 'light';
    document.cookie = "theme_mode=" + themeMode + ";path=/";

    var themeIcon = document.getElementById('toggleicon');
    if (themeMode === 'dark') {
        themeIcon.classList.remove('fa-moon-o');
        themeIcon.classList.add('fa-sun-o');
    } else {
        themeIcon.classList.remove('fa-sun-o');
        themeIcon.classList.add('fa-moon-o');
    }


}

// JavaScript code to apply theme mode
document.addEventListener("DOMContentLoaded", function () {
    // Retrieve user's preferred theme mode from cookie, default to 'light' if not set
    var themeMode = document.cookie.replace(/(?:(?:^|.*;\s*)theme_mode\s*=\s*([^;]*).*$)|^.*$/, "$1") || 'light';

    // Apply appropriate theme mode styles
    if (themeMode === 'dark') {
        document.body.classList.add('dark-mode');  // Apply dark mode styles
    }


    var themeIcon = document.getElementById('toggleicon');
    if (themeMode === 'dark') {
        themeIcon.classList.remove('fa-moon-o');
        themeIcon.classList.add('fa-sun-o');
    } else {
        themeIcon.classList.remove('fa-sun-o');
        themeIcon.classList.add('fa-moon-o');

    }
});

function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}



function logoutbar() {
    let logout = document.getElementById("logout-bar");
    if (logout.style.display === "block") {
        logout.style.display = "none";
    } else {
        logout.style.display = "block";
    }
}

function displaynev() {
    let navlst = document.getElementById("nav-list-div");
    let navbutton = document.getElementById("navbutton");
    let navlstDisplay = window.getComputedStyle(navlst).display;

    if (navlstDisplay === "none") {
        navlst.style.display = "block"; // Show the nav list
        navbutton.style.display = "none"; // Hide the nav button
    } else {
        navlst.style.display = "none"; // Hide the nav list
        navbutton.style.display = "flex"; // Show the nav button
    }
}







// chefsprofile.html
function toggleRatingForm() {

    document.getElementById('star-rating').style.display = "None";
    document.getElementById('rating-form').style.display = 'Block';
  }

  function displayFilterForm() {

    let filterform = document.getElementById("filterform");
    filterform.style.display = filterform.style.display === "none" ? "block" : "none";
  }


 // recipe.html

 function toggleSortBar() {
    let sortBar = document.getElementById("sort-bar");
    sortBar.style.display = sortBar.style.display === "block" ? "none" : "block";
}



function displayFilterForm() {

    let filterform = document.getElementById("filterform");
    filterform.style.display = filterform.style.display === "none" ? "block" : "none";
}


