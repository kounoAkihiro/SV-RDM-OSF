from nose.tools import *
from modularodm import Q

from scripts.set_comment_modified_default_false import get_targets, do_migration
from tests.base import OsfTestCase
from tests.factories import CommentFactory
from website.project.model import Comment


class TestUpdateDefaultCommentModified(OsfTestCase):

    def test_get_targets(self):
        comment = CommentFactory(modified=None)
        modified_comment = CommentFactory(modified=True)
        targets = Comment.find(Q('modified', 'eq', None))
        assert_equal(targets.count(), 1)

    def test_unmodified_comment_default_is_set_to_false(self):
        comment = CommentFactory(modified=None)
        do_migration(get_targets(), dry=False)
        comment.reload()
        assert_equal(comment.modified, False)

    def test_modified_comment_does_not_update(self):
        comment = CommentFactory(modified=True)
        do_migration(get_targets(), dry=False)
        assert_true(comment.modified)

    def test_update_default_modified_updates_all_targets(self):
        comment = CommentFactory(modified=None)
        targets = Comment.find(Q('modified', 'eq', None))
        assert_equal(targets.count(), 1)

        do_migration(get_targets(), dry=False)
        assert_equal(targets.count(), 0)