/**
 * Github FileBrowser configuration module.
 */
(function(Rubeus) {

    // Private members

    function refreshGitHubTree(grid, item, branch) {
        var data = item.data || {};
        data.branch = branch;
        var url = item.urls.branch + '?' + $.param({branch: branch});
        $.ajax({
            type: 'get',
            url: url,
            success: function(data) {
                // Update the item with the new branch data
                $.extend(item, data);
                grid.reloadFolder(item);
            }
        });
    }

    // Register configuration
    Rubeus.cfg.github = {
        // Handle changing the branch select
        listeners: [{
            on: 'change',
            selector: '.github-branch-select',
            callback: function(evt, row, grid) {
                var $this = $(evt.target);
                var branch = $this.val();
                refreshGitHubTree(grid, row, branch);
            }
        }],
        maxFilesize: 10
    };

})(Rubeus);
