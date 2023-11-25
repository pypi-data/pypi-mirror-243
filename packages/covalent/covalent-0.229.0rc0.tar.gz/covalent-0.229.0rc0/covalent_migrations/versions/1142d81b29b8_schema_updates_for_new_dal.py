# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Schema updates for new DAL

Revision ID: 1142d81b29b8
Revises: de0a6c0a3e3d
Create Date: 2023-06-18 09:18:31.450740

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pragma: allowlist nextline secret
revision = "1142d81b29b8"
# pragma: allowlist nextline secret
down_revision = "de0a6c0a3e3d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("storage_type", sa.Text(), nullable=False),
        sa.Column("storage_path", sa.Text(), nullable=False),
        sa.Column("object_key", sa.Text(), nullable=False),
        sa.Column("digest_alg", sa.Text(), nullable=True),
        sa.Column("digest", sa.Text(), nullable=True),
        sa.Column("remote_uri", sa.Text(), nullable=True),
        sa.Column("size", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lattice_assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meta_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=24), nullable=False),
        sa.Index("lattice_assets_idx", "meta_id", "key"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], name="asset_link"),
        sa.ForeignKeyConstraint(["meta_id"], ["lattices.id"], name="lattice_link"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "electron_assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meta_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=24), nullable=False),
        sa.Index("electron_assets_idx", "meta_id", "key"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], name="asset_link"),
        sa.ForeignKeyConstraint(["meta_id"], ["electrons.id"], name="electron_link"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("electron_dependency", schema=None) as batch_op:
        batch_op.create_index("cnode_idx", ["electron_id"], unique=False)
        batch_op.create_index("pnode_idx", ["parent_electron_id"], unique=False)
        batch_op.create_foreign_key(
            "parent_electron_link", "electrons", ["parent_electron_id"], ["id"]
        )

    with op.batch_alter_table("electrons", schema=None) as batch_op:
        batch_op.add_column(sa.Column("task_group_id", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("executor_data", sa.Text(), nullable=True))
        batch_op.create_index(
            "latid_nodeid_idx", ["parent_lattice_id", "transport_graph_node_id"], unique=False
        )
        batch_op.drop_column("executor_data_filename")

    with op.batch_alter_table("jobs", schema=None) as batch_op:
        batch_op.add_column(sa.Column("status", sa.String(length=24), nullable=False))
        batch_op.drop_column("cancel_successful")

    with op.batch_alter_table("lattices", schema=None) as batch_op:
        batch_op.add_column(sa.Column("executor_data", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("workflow_executor_data", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("python_version", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("covalent_version", sa.Text(), nullable=True))
        batch_op.create_unique_constraint("u_dispatch_id", ["dispatch_id"])
        batch_op.drop_column("executor_data_filename")
        batch_op.drop_column("workflow_executor_data_filename")
        batch_op.drop_column("transport_graph_filename")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("lattices", schema=None) as batch_op:
        batch_op.add_column(sa.Column("transport_graph_filename", sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column("workflow_executor_data_filename", sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column("executor_data_filename", sa.TEXT(), nullable=True))
        batch_op.drop_constraint("u_dispatch_id", type_="unique")
        batch_op.drop_column("covalent_version")
        batch_op.drop_column("python_version")
        batch_op.drop_column("workflow_executor_data")
        batch_op.drop_column("executor_data")

    with op.batch_alter_table("jobs", schema=None) as batch_op:
        batch_op.add_column(sa.Column("cancel_successful", sa.BOOLEAN(), nullable=False))
        batch_op.drop_column("status")

    with op.batch_alter_table("electrons", schema=None) as batch_op:
        batch_op.add_column(sa.Column("executor_data_filename", sa.TEXT(), nullable=True))
        batch_op.drop_index("latid_nodeid_idx")
        batch_op.drop_column("executor_data")
        batch_op.drop_column("task_group_id")

    with op.batch_alter_table("electron_dependency", schema=None) as batch_op:
        batch_op.drop_constraint("parent_electron_link", type_="foreignkey")
        batch_op.drop_index("pnode_idx")
        batch_op.drop_index("cnode_idx")

    op.drop_table("electron_assets")
    op.drop_table("lattice_assets")
    op.drop_table("assets")
    # ### end Alembic commands ###
