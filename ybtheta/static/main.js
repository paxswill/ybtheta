$(function() {
	$('a#edit').bind('click', function() {
		$('dl.edit-toggle').css('display', 'none');
		$('form.edit-toggle').css('display', 'inherit');
		return false;
	});
});
$(function() {
	$('a#cancel').bind('click', function() {
		$('dl.edit-toggle').css('display', 'inherit');
		$('form.edit-toggle').css('display', 'none');
		return false;
	});
});
