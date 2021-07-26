$(document).ready(function(){

	var csrfToken = $('#ajax').find('input[name="csrfmiddlewaretoken"]').val();
	var ajax_button = $('#ajax');
	var ajax_elements_count = $('.table-kid').length;
	var table_container = $('.table');
	var filter_form = $('#filter-form');

	var csrf = 0;
	var markets = [];
	var profitUp = 0;
	var profitDown = 0;
	var volume = 0;

	ajax_button.submit(function(){
		var ffd = filter_form.serialize();

		$.ajax({
			url: "/accept-ajax/",
			type: 'POST',
			data: {
				'p': ajax_elements_count/20,
				'data' : ffd
			},
			dataType: 'JSON',
			headers: {'X-CSRFToken': csrfToken},
			success: function(data, status, xhr) {
				console.log(data);
				for (var i = 0; i <= data['objs'].length - 1; i++) {
					var el = data['objs'][i];

					var tmp = $("<tr class='m-2 table-kid'><td class='ml-3'>" +
						"<a href='https://www.coingecko.com/en/coins/" + el.coin.toLowerCase().replace(/ /gi, '-') + "#markets' target='_blank'>"+el.coin+"</a></td>"+
				"<td class='ml-3'>" + el.market1 + "</td>"+
				"<td class='ml-3'>" + el.market2 + "</td>"+
				"<td class='ml-3'>" + el.volume + "</td>"+
				"<td class='ml-3'>" + el.profit + "</td></tr>");
					table_container.append(tmp);

				}
				ajax_elements_count = $('.table-kid').length;
				return false
			}
		});
		return false;
	});
});
