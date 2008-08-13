<?php
query_posts('cat=7&orderby=title&order=asc&posts_per_page=-1');
 ?>
 
<?php while (have_posts()) : the_post(); ?>
<div class="post">
        <h3 id="post-<?php the_ID(); ?>">
        <a href="<?php the_permalink() ?>" rel="bookmark" title="Permanent Link to <?php the_title_attribute(); ?>"><?php the_title(); ?></a></h3>

        <div class="excerpt">
            <?php the_excerpt(); ?>
        </div>

    </div>
<?php endwhile; ?>

<?php
query_posts('posts_per_page=1');
 ?>
