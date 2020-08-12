/**
 * Navbar Burger
 */
document.addEventListener('DOMContentLoaded', () => {
	const menus = document.querySelectorAll('.navbar-burger');
	const dropdowns = document.querySelectorAll('.navbar-menu');
	console.log(dropdowns.length)
	if (menus.length && dropdowns.length) {
			for (var i = 0; i < menus.length; i++) {
					menus[i].addEventListener('click', function() {
							for (var j = 0; j < dropdowns.length; j++) {
									dropdowns[j].classList.toggle('is-active');
							}
					});
			}
	}
});