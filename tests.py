import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope='session')
def driver(request):
    _driver = webdriver.PhantomJS()
    _driver.get('http://atomicboard.devman.org/create_test_user/')
    _driver.find_element_by_tag_name('button').click()
    WebDriverWait(_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/p[2]')))
    _driver.get('http://atomicboard.devman.org/#/')
    WebDriverWait(_driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'js-ticket')))

    def driver_teardown():
        _driver.quit()
    request.addfinalizer(driver_teardown)
    return _driver


def test_loading_and_displaying_tickets(driver):
    assert len(driver.find_elements_by_class_name('js-ticket')) > 0


def test_drag_and_drop_ticket(driver):
    source_idx, target_idx = 0, 1
    columns = driver.find_elements_by_class_name('tickets-column')
    ticket = columns[0].find_element_by_class_name('js-ticket')
    ticket_id = ticket.find_element_by_class_name('ticket_id').text

    # HTML5 Drag and Drop is not currently supported by Selenium
    # https://stackoverflow.com/a/29381532/4627579
    # https://gist.github.com/rcorreia/2362544
    with open('drag_and_drop_helper.js') as f:
        drag_and_drop_js = f.read()
    drag_and_drop_js += '''$('.js-ticket').simulateDragDrop({sourceIndex: %d,
                                                             dropTarget: '.tickets-column',
                                                             targetIndex: %d});
    ''' % (source_idx, target_idx)
    driver.execute_script(drag_and_drop_js)
    assert any(ticket_id == _ticket.find_element_by_class_name('ticket_id').text
               for _ticket in columns[target_idx].find_elements_by_class_name('js-ticket'))


def test_ticket_editing(driver):
    text = 'test'
    ticket_header = driver.find_element_by_class_name('panel-heading_text')
    ticket_text = ticket_header.text
    ticket_header.click()
    ticket_input = driver.find_element_by_class_name('editable-input')
    ticket_input.send_keys('{}{}'.format(text, Keys.RETURN))
    assert ticket_header.text == ticket_text + text


def test_marking_ticket_as_solved(driver):
    ticket_status = driver.find_element_by_class_name('ticket_status')
    ticket_status.click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'change-status-form__button')))
    btn_close = driver.find_elements_by_class_name('change-status-form__button')[2]
    btn_close.click()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'js-change-status-form')))
    assert ticket_status.text == 'closed'


def test_creating_new_ticket(driver):
    text = 'creating new ticket'
    expected_tickets_count = len(driver.find_elements_by_class_name('js-ticket')) + 1
    btn_add_ticket = driver.find_element_by_class_name('add-ticket-block_button')
    btn_add_ticket.click()
    ticket_input = driver.find_element_by_class_name('editable-input')
    ticket_input.send_keys('{}{}'.format(text, Keys.RETURN))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(.,"{}")]'.format(text))))
    assert expected_tickets_count == len(driver.find_elements_by_class_name('js-ticket'))
