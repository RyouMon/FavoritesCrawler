from favorites_crawler.utils.cookies import load_cookie


class TestLoadCookie:
    def test_load_cookie_when_file_exists(self, tmp_path):
        domain = 'localhost'
        cookie_file = tmp_path / f'{domain}_cookies.txt'
        cookie_file.touch()
        cookie_file.write_text(
            """# Netscape HTTP Cookie File
            # http://curl.haxx.se/rfc/cookie_spec.html
            # This is a generated file!  Do not edit.
    
            localhost	FALSE	/	TRUE	9933144989	User-Agent	Test
            """
        )

        cookie = load_cookie(domain, tmp_path)

        assert cookie == {'User-Agent': 'Test'}

    def test_load_cookie_when_file_not_exists(self, tmp_path):
        domain = 'localhost'

        cookie = load_cookie(domain, tmp_path)

        assert cookie == {}

    def test_load_cookie_when_file_invalid(self, tmp_path):
        domain = 'localhost'
        cookie_file = tmp_path / f'{domain}_cookies.txt'
        cookie_file.touch()
        cookie_file.write_text('')
        cookie = load_cookie(domain, tmp_path)

        assert cookie == {}
