let center = [55.4300079452529, 37.55061844019641];

function init() {
    let map = new ymaps.Map('map-test', {
        center: center,
        zoom: 14
    });

    let placemark = new ymaps.Placemark(center, {
        balloonContentHeader: 'Хедер балуна',
		balloonContentBody: 'Боди балуна',
		balloonContentFooter: 'Подвал',
    }, {
        iconLayout: 'default#image',
		iconImageHref: 'https://static.tildacdn.com/tild3133-3831-4364-b931-353139306562/pin-icon-on-white-ba.png',
		iconImageSize: [40, 40],
		iconImageOffset: [-19, -44]

    });

    let placemark1 = new ymaps.Placemark(center, {
        balloonContent: `

			<div class="balloon text_map">
				<div class="balloon__address">г. Подольск</div>
				<div class="balloon__contacts">
					<a href="tel:+7 800 707-37-27">+7 800 707-37-27</a>
				</div>
			</div>

		`
    }, {
        iconLayout: 'default#image',
		iconImageHref: 'https://static.tildacdn.com/tild3133-3831-4364-b931-353139306562/pin-icon-on-white-ba.png',
		iconImageSize: [40, 40],
		iconImageOffset: [-19, -44]

    });

    map.controls.remove('geolocationControl'); // удаляем геолокацию
    map.controls.remove('searchControl'); // удаляем поиск
    map.controls.remove('trafficControl'); // удаляем контроль трафика
    map.controls.remove('typeSelector'); // удаляем тип
    map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
    map.controls.remove('zoomControl'); // удаляем контрол зуммирования
    map.controls.remove('rulerControl'); // удаляем контрол правил
    // map.behaviors.disable(['scrollZoom']); // отключаем скролл карты (опционально)

    // map.geoObjects.add(placemark);
    map.geoObjects.add(placemark1);
    // placemark1.balloon.open();
}

ymaps.ready(init);