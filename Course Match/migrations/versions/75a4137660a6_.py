"""empty message

Revision ID: 75a4137660a6
Revises: None
Create Date: 2016-05-20 21:34:57.736000

"""

# revision identifiers, used by Alembic.
revision = '75a4137660a6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('course_id', sa.String(length=10), nullable=True),
    sa.Column('teacher', sa.String(length=20), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_class_course_id'), 'class', ['course_id'], unique=False)
    op.create_index(op.f('ix_class_name'), 'class', ['name'], unique=False)
    op.create_index(op.f('ix_class_teacher'), 'class', ['teacher'], unique=False)
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teacher_name'), 'teacher', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('student_assosiate_table',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('teacher_assosiate_table',
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_assosiate_table')
    op.drop_table('student_assosiate_table')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_teacher_name'), table_name='teacher')
    op.drop_table('teacher')
    op.drop_index(op.f('ix_class_teacher'), table_name='class')
    op.drop_index(op.f('ix_class_name'), table_name='class')
    op.drop_index(op.f('ix_class_course_id'), table_name='class')
    op.drop_table('class')
    ### end Alembic commands ###
