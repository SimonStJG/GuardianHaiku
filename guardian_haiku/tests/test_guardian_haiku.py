from guardian_haiku.guardian_haiku import main
import tempfile


class TestFunctional(object):
    """Functional tests for guardian_haiku."""

    def test_logging(self):
        logfile_suffix = "functional_test"
        with tempfile.TemporaryDirectory() as tmpdir_name:
            try:
                main(log_dir_root=tmpdir_name,
                     logfile_suffix=logfile_suffix,
                     rss_feed_url="http://localhost")
            # TODO This is a crap test atm
            except Exception:
                pass

            with open("{tmpdir_name}/guardian_haiku/guardian_haiku."
                      "{logfile_suffix}.log".format(**locals())) as f:
                assert "guardian_haiku running" in f.readline()
